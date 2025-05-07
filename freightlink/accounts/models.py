from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone_number, email, password=None, **extra_fields):
        """Create and save a User with the given phone_number, email and password."""
        if not phone_number:
            raise ValueError('The given phone number must be set')
        email = self.normalize_email(email) if email else None
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        """Create and save a regular User with the given phone_number, email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        """Create and save a SuperUser with the given phone_number, email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with phone authentication instead of username."""
    
    USER_TYPE_CHOICES = (
        ('business', 'Business User'),
        ('truck_owner', 'Truck Owner'),
        ('admin', 'Administrator'),
    )
    
    # Remove username as we'll use phone_number instead
    username = None
    
    # Basic fields
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        unique=True,
        verbose_name=_('phone number')
    )
    email = models.EmailField(_('email address'), blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='business')
    
    # Profile fields
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    business_registration_number = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # Location fields
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Verification fields
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_code_expires = models.DateTimeField(blank=True, null=True)
    
    # Communication preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    
    # Platform metrics
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Last online timestamp
    last_online = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.get_full_name() or self.phone_number} - {self.user_type}"
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']


class BusinessDocument(models.Model):
    """Documents for business verification."""
    
    DOCUMENT_TYPE_CHOICES = (
        ('business_registration', 'Business Registration'),
        ('id_document', 'ID Document'),
        ('tax_certificate', 'Tax Certificate'),
        ('other', 'Other Document'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_documents')
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    document = models.FileField(upload_to='verification_docs/')
    is_verified = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.document_type} for {self.user.phone_number}"
    
    class Meta:
        ordering = ['-uploaded_at']


class UserVerification(models.Model):
    """Verification history for users."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_history')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name='verifications_processed',
        blank=True, 
        null=True
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Verification for {self.user.phone_number} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']