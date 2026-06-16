
from rest_framework import generics
from .serializer import UserCreateSerializer,UserCreateEmployeeSerializer,changePasswordSerializer,MyTokenObtainPairSerializer,EmployeeSerializer
from .service import verification_user,employee_create,change_password,force_password_change_by_founder,password_change_by_founder_of_employee,get_all_employees,get_all_employee__organization,list_employee
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import is_temp_pass,Founder_Set_Up,employeeDeletePermission,employee_view_permission,employee_verification
from rest_framework_simplejwt.views import TokenObtainPairView
from streak.service import create_streak
from django.db import transaction,IntegrityError
from rest_framework.exceptions import ValidationError
from verification.service import EmailVerification
# --- DRF-SPECTACULAR IMPORTS ---
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse, OpenApiExample
from .models import employees


# Create your views here.


@extend_schema_view(
    post=extend_schema(
        summary="Register a new Founder Account",
        description="Creates a base employee user record with a 'Founder' architectural role. Triggers automatic streak initialization and sends a verification link to the registered email address. Account remains unverified until email confirmation.",
        tags=["User Authentication & Management"],
        responses={
            201: OpenApiResponse(response=UserCreateSerializer, description="Founder account successfully created. Verification email dispatched."),
            400: OpenApiResponse(description="Invalid request parameter format, missing required field, or username/email duplication conflicts.")
        }
    )
)
class CreateUser(generics.CreateAPIView):
    queryset=get_all_employees()
    serializer_class=UserCreateSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        try:

            user=serializer.save()
            create_streak(serializer.data['id'])
            transaction.on_commit(
                lambda:EmailVerification(self.request,user.email,user)
            )
        except IntegrityError:
            raise ValidationError('could not create the user')
        
    
@extend_schema_view(
    get=extend_schema(
        summary="Retrieve specific Employee record",
        description="Fetch explicit profile parameters of a singular worker using their unique database primary key ID. Access restricted by organizational boundaries.",
        tags=["Employee Profiles"],
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH, description="The sequential database ID integer representing the target employee record.")
        ],
        responses={
            200: OpenApiResponse(response=EmployeeSerializer, description="Detailed profile attributes parsed successfully."),
            401: OpenApiResponse(description="Provided Bearer JWT token is invalid or has expired."),
            403: OpenApiResponse(description="Access denied. User lacks permission validation rules to inspect this profile instance."),
            440: OpenApiResponse(description="Action locked. Access restricted until account completes formal email verification parameters.")
        }
    )
)
class employee_retrieve(generics.RetrieveAPIView):
    queryset=get_all_employee__organization()
    serializer_class=EmployeeSerializer
    lookup_field='pk'
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,employee_verification,employee_view_permission]
    def retrieve(self, request, *args, **kwargs):
        
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            raise ValidationError({
                'error':'could not get the employee',
                'details':str(e)
            })

@extend_schema_view(
    get=extend_schema(
        summary="List all organization Employees",
        description="Returns an array catalog of all active workers assigned within the authenticated administrator's corporate organization instance.",
        tags=["Employee Profiles"],
        responses={
            200: OpenApiResponse(response=EmployeeSerializer(many=True), description="List array of worker definitions returned successfully.")
        }
    )
)
class employee_list(generics.ListAPIView):
    queryset=get_all_employee__organization()
    serializer_class=EmployeeSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,employee_verification]
    def list(self, request, *args, **kwargs):
        return list_employee(self, request, *args, **kwargs)



@extend_schema_view(
    get=extend_schema(
        summary="Verify Account Email Address",
        description="Validates a newly created Founder profile by checking the parameter signature token passed within the verification link query parameters.",
        tags=["User Authentication & Management"],
        responses={
            200: OpenApiResponse(description="Account verified. System profile fully activated for live authorization state access.")
        }
    )
)
class Verification(generics.RetrieveAPIView):
    queryset=get_all_employees()
    serializer_class=UserCreateSerializer
    def retrieve(self, request, *args, **kwargs):
        return verification_user(self, request, *args, **kwargs)
        



@extend_schema_view(
    post=extend_schema(
        summary="Onboard an Employee (Founder Action)",
        description="Allows authenticated Founders to manually provision employee user profiles within their specific organization. Profiles default to a temporary password status, requiring an update upon initial system authentication.",
        tags=["Founder Management Controls"],
        request=UserCreateEmployeeSerializer,
        responses={
            201: OpenApiResponse(response=UserCreateEmployeeSerializer, description="Temporary employee record registered successfully."),
            403: OpenApiResponse(description="Access restricted. Only authenticated profiles with active Founder credentials can initiate this action.")
        }
    )
)
class EmployeeTemperary(generics.CreateAPIView):
    queryset=get_all_employees()
    serializer_class=UserCreateEmployeeSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,Founder_Set_Up]
    def create(self, request, *args, **kwargs):
        return employee_create(self, request, *args, **kwargs)
    



@extend_schema_view(
    put=extend_schema(
        summary="Update Account Password",
        description="Enables workers provisioned with a temporary status flag to update their credentials. Resolves the temporary status barrier to unlock full system route access.",
        tags=["User Authentication & Management"],
        request=changePasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password modified successfully. Credentials updated.")
        }
    ),
    patch=extend_schema(exclude=True) # Exclude PATCH method visual noise if view only utilizes PUT
)
class changePassword(generics.UpdateAPIView):
    serializer_class=changePasswordSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,is_temp_pass]
    def update(self, request, *args, **kwargs):
        return change_password(self, request, *args, **kwargs)
    


@extend_schema_view(
    put=extend_schema(
        summary="Force User Password Reset Request",
        description="Administrative tool allowing an authorized Founder to invalidate an employee profile's current login credentials, forcing a temporary reset state.",
        tags=["Founder Management Controls"],
        responses={
            200: OpenApiResponse(description="Target account credentials flagged for immediate password reset.")
        }
    ),
    patch=extend_schema(exclude=True)
)
class force_password_reset(generics.UpdateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,Founder_Set_Up]
    def update(self, request, *args, **kwargs):
        return force_password_change_by_founder(self, request, *args, **kwargs)



@extend_schema_view(
    put=extend_schema(
        summary="Override Employee Password Directly",
        description="Allows a Founder to overwrite credentials for a specific employee sub-account within their organization.",
        tags=["Founder Management Controls"],
        request=changePasswordSerializer,
        responses={
            200: OpenApiResponse(description="Target employee password overwritten successfully.")
        }
    ),
    patch=extend_schema(exclude=True)
)
class changePasswordByFounder(generics.UpdateAPIView):
    queryset=get_all_employees()
    serializer_class=changePasswordSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,Founder_Set_Up]
    def update(self, request, *args, **kwargs):
        return password_change_by_founder_of_employee(self, request, *args, **kwargs)
        

@extend_schema_view(
    post=extend_schema(
        summary="Generate System Access Tokens (Login)",
        description="Validates raw user login criteria against database user structures. Returns a signed JWT token package containing pairs for runtime authorization headers.",
        tags=["User Authentication & Management"],
        responses={
            200: OpenApiResponse(
                description="Pair tokens authenticated. Use the 'access' token value within application header configurations.",
                examples=[
                    OpenApiExample(
                        name="Successful Authentication Response",
                        value={
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                        }
                    )
                ]
            )
        }
    )
)
class mytoken(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
        

@extend_schema_view(
    delete=extend_schema(
        summary="Offboard / Delete an Employee Profile",
        description="Removes an employee user account from the system registry database permanently.",
        tags=["Founder Management Controls"],
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH, description="The unique database tracking ID integer of the worker profile to be removed.")
        ],
        responses={
            204: OpenApiResponse(description="Employee account dropped from organization registries successfully."),
            403: OpenApiResponse(description="Action blocked. Current credentials lack clearance validation to delete this user entry.")
        }
    )
) 
class employeeDelete(generics.DestroyAPIView):
    queryset=get_all_employees()
    lookup_field='pk'
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,employeeDeletePermission]

