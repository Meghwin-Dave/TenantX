# User Access Scope Profile Guide

## Overview

The User Access Scope Profile functionality allows you to create predefined access profiles that can be applied to users, automatically populating their access scopes. This provides a consistent and efficient way to manage user permissions across the TenantX system.

## Features

### 🎯 **Profile Management**
- Create reusable access scope profiles
- Define multiple access scopes per profile
- Support for all TenantX doctypes (Enterprise, SBU, Factory, etc.)
- Granular read/write permissions

### 🔄 **Automatic Population**
- Select a profile to automatically populate user access scopes
- Clear existing scopes before applying new ones
- Real-time validation and error handling
- Success/error notifications

### ✅ **Validation & Quality Control**
- Validate profile configurations
- Check user access scope integrity
- Comprehensive error reporting
- Warning system for potential issues

## How to Use

### 1. Creating a User Access Scope Profile

1. **Navigate to**: TenantX > User Access Scope Profile
2. **Create New Profile**:
   - Enter a descriptive name for the profile
   - Add access details in the child table

3. **Configure Access Details**:
   - **Scope Type**: Select the doctype (Enterprise, SBU, Factory, etc.)
   - **Scope Name**: Choose the specific record from the selected doctype
   - **Read**: Check to grant read permissions
   - **Write**: Check to grant write permissions

4. **Save the Profile**

### 2. Applying Profile to User

1. **Navigate to**: User Management > User
2. **Select or Create User**
3. **Go to User Access Section**:
   - Find the "User Access" section in the user form
   - Select a "User Access Scope Profile" from the dropdown

4. **Automatic Population**:
   - The system will automatically populate the "User Access Scope" child table
   - All access details from the selected profile will be copied
   - A success message will confirm the operation

### 3. Manual Controls

The User form provides several buttons for managing access scopes:

- **Populate from Profile**: Manually trigger profile population
- **Clear Access Scope**: Remove all access scopes from the user
- **Validate Access Scope**: Check for configuration issues

## Supported Scope Types

The following TenantX doctypes can be used as scope types:

- **Enterprise**: Access to specific enterprises
- **Strategic Business Unit (SBU)**: Access to specific SBUs
- **Factory Business Unit**: Access to specific factories

## API Methods

### Get Access Scope from Profile
```python
from tenantx.api import get_user_access_scope_from_profile

access_details = get_user_access_scope_from_profile("Profile Name")
```

### Apply Profile to User
```python
from tenantx.api import apply_profile_to_user

result = apply_profile_to_user("user@example.com", "Profile Name")
```

### Validate User Access Scope
```python
from tenantx.api import validate_user_access_scope

validation = validate_user_access_scope("user@example.com")
```

### Get Available Profiles
```python
from tenantx.api import get_available_profiles

profiles = get_available_profiles()
```

## Validation Rules

### Profile Validation
- Access details cannot be empty
- Scope type and scope name are required
- Scope name must exist in the specified doctype
- Only Enterprise, Strategic Business Unit, and Factory Business Unit are allowed as scope types

### User Access Scope Validation
- At least one permission (read or write) must be granted
- Scope references must be valid
- Missing scope types or names are flagged as errors

## Best Practices

### 1. **Profile Naming**
- Use descriptive names that indicate the access level
- Examples: "Manager Access", "Viewer Access", "Factory Supervisor"

### 2. **Permission Design**
- Grant minimum required permissions
- Use read-only access for viewers
- Reserve write access for authorized personnel

### 3. **Profile Organization**
- Create profiles for common roles
- Use hierarchical naming (e.g., "Enterprise Manager - Electronics")
- Document profile purposes and usage

### 4. **Regular Validation**
- Periodically validate user access scopes
- Check for orphaned references
- Review and update profiles as needed

## Troubleshooting

### Common Issues

1. **Profile Not Found**
   - Ensure the profile exists and is active
   - Check for typos in profile names

2. **Access Scopes Not Populating**
   - Verify the profile has access details configured
   - Check browser console for JavaScript errors

3. **Validation Errors**
   - Ensure all scope references are valid
   - Check that required fields are filled

4. **Permission Issues**
   - Verify user has System Manager role
   - Check custom field permissions

### Error Messages

- **"Profile does not exist"**: Profile name is incorrect or profile is deleted
- **"No access scopes found"**: Profile has no access details configured
- **"Scope does not exist"**: Referenced record has been deleted
- **"Invalid scope type"**: Selected doctype is not supported

## Technical Details

### Database Structure
- **User Access Scope Profile**: Master profile definitions
- **User Access Scope**: Child table storing user-specific access details
- **Custom Fields**: User form extensions for profile selection

### JavaScript Integration
- Automatic population on profile selection
- Real-time validation and error handling
- User-friendly notifications and progress indicators

### API Endpoints
- RESTful API methods for profile management
- Comprehensive error handling and validation
- Support for bulk operations

## Security Considerations

1. **Permission Validation**: All API methods validate user permissions
2. **Data Integrity**: Automatic validation prevents invalid configurations
3. **Audit Trail**: All changes are tracked in the system
4. **Access Control**: Only authorized users can modify profiles

## Support

For technical support or questions:
- Email: meghwin@cognitionx.tech
- Publisher: CognitionXLogic

---

**Note**: This functionality is part of the TenantX application and requires proper installation and configuration of the TenantX app. 