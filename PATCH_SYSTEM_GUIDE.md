# TenantX Patch System Guide

## Overview

The TenantX patch system automatically sets up roles and permissions during Frappe migrations, ensuring that your permission system is properly configured without manual intervention.

## How It Works

### 1. **Patch File Location**
```
apps/tenantx/tenantx/patches/v1_0_0_setup_roles_and_permissions.py
```

### 2. **Patch Registration**
The patch is registered in `patches.txt`:
```
[post_model_sync]
tenantx.tenantx.patches.v1_0_0_setup_roles_and_permissions
```

### 3. **Execution Timing**
- **When**: After all DocTypes are migrated (`post_model_sync`)
- **Why**: Ensures all required DocTypes exist before setting up permissions

## What the Patch Does

### **Phase 1: Core Roles Creation**
Creates the essential roles for TenantX:
- ✅ Enterprise Admin
- ✅ SBU Head  
- ✅ Factory Head
- ✅ Factory User
- ✅ Liaison Officer

### **Phase 2: Role Permissions**
Sets up DocType permissions for each role:
```python
# Example: SBU Head permissions
"SBU Head": {
    "Strategic Business Unit": ["read", "write", "create", "submit", "cancel", "amend"],
    "Factory Business Unit": ["read", "write", "create", "submit", "cancel", "amend"],
    "Purchase Order": ["read", "write", "create", "submit", "cancel"],
    # ... more permissions
}
```

### **Phase 3: Field-Level Permissions**
Sets permission levels for sensitive fields:
```python
# Example: Factory Business Unit fields
"Factory Business Unit": {
    "capacity": {"permission_level": 1},
    "cost_center": {"permission_level": 1},
    "factory_head": {"permission_level": 1}
}
```

### **Phase 4: Test Users (Optional)**
Creates test users for each role (configurable):
- enterprise.admin@test.com
- sbu.head@test.com
- factory.head@test.com
- factory.user@test.com
- liaison.officer@test.com

## Configuration Options

### **Environment Variables**
You can control patch behavior using Frappe configuration:

```python
# In your site_config.json or common_site_config.json
{
    "tenantx_create_test_users": true,
    "tenantx_show_setup_messages": true,
    "tenantx_detailed_logging": true,
    "tenantx_fail_on_error": false,
    "tenantx_create_test_users_production": false
}
```

### **Configuration Options**

| Option | Default | Description |
|--------|---------|-------------|
| `tenantx_create_test_users` | `true` | Whether to create test users |
| `tenantx_show_setup_messages` | `true` | Show setup completion messages |
| `tenantx_detailed_logging` | `true` | Log detailed patch information |
| `tenantx_fail_on_error` | `false` | Fail migration if patch encounters errors |
| `tenantx_create_test_users_production` | `false` | Create test users in production |

## When Patches Run

### **Automatic Execution**
Patches run automatically during:
- `bench migrate` - Database migrations
- `bench --site site.com migrate` - Site-specific migrations
- App installation/update

### **Manual Execution**
You can also run patches manually:
```bash
# Run all patches
bench --site site.com execute tenantx.tenantx.patches.v1_0_0_setup_roles_and_permissions.execute

# Run specific patch
bench --site site.com execute tenantx.tenantx.patches.v1_0_0_setup_roles_and_permissions.execute
```

## Patch Safety Features

### **1. Duplicate Prevention**
```python
def create_role_if_not_exists(role_data):
    role_name = role_data["role_name"]
    
    if not frappe.db.exists("Role", role_name):
        # Create role only if it doesn't exist
        role_doc = frappe.get_doc({...})
        role_doc.insert(ignore_permissions=True)
    else:
        frappe.logger().info(f"Role already exists: {role_name}")
```

### **2. Error Handling**
```python
try:
    # Patch execution
    setup_core_roles()
    setup_role_permissions()
    # ...
except Exception as e:
    frappe.logger().error(f"Error in TenantX roles setup patch: {str(e)}")
    # Don't fail the migration, just log the error
    frappe.msgprint("Warning: Setup encountered an error...")
```

### **3. Production Safety**
```python
def should_create_test_users():
    # Don't create test users in production unless explicitly enabled
    if is_production() and not frappe.conf.get('tenantx_create_test_users_production', False):
        return False
    return config.get('create_test_users', True)
```

## Patch Output

### **Success Output**
```
Starting TenantX Roles and Permissions Setup...
Setting up core roles...
Created role: Enterprise Admin
Created role: SBU Head
Created role: Factory Head
Created role: Factory User
Created role: Liaison Officer
Setting up role permissions...
Setting permissions for role: Enterprise Admin
  Set permissions for Enterprise
  Set permissions for Strategic Business Unit
  ...
Setting up field level permissions...
  Set permission level 1 for Factory Business Unit.capacity
  ...
Creating test users...
Created test user: enterprise.admin@test.com with role: Enterprise Admin
...
TenantX Roles and Permissions Setup completed successfully!
```

### **Error Output**
```
Error in TenantX roles setup patch: [Error details]
Warning: TenantX roles setup encountered an error. 
Please run the setup manually: from tenantx.tenantx.setup_roles import run_full_setup
```

## Verification Steps

### **Check Roles Created**
```python
# In Frappe console
roles = frappe.get_list("Role", filters={
    "role_name": ["in", ["Enterprise Admin", "SBU Head", "Factory Head", "Factory User", "Liaison Officer"]]
})
print(f"Created {len(roles)} roles")
```

### **Check Permissions Created**
```python
# Check SBU Head permissions
sbu_permissions = frappe.get_list("Custom DocPerm", filters={"role": "SBU Head"})
print(f"SBU Head has {len(sbu_permissions)} DocType permissions")
```

### **Check Test Users**
```python
# Check if test users were created
test_users = frappe.get_list("User", filters={
    "email": ["like", "%@test.com"]
})
print(f"Created {len(test_users)} test users")
```

## Troubleshooting

### **Common Issues**

1. **Patch not running**:
   - Check if patch is registered in `patches.txt`
   - Verify patch file exists in correct location
   - Check Frappe logs for errors

2. **Roles not created**:
   - Check if roles already exist
   - Verify user has sufficient permissions
   - Check for syntax errors in patch file

3. **Permissions not set**:
   - Ensure DocTypes exist before patch runs
   - Check if Custom DocPerm records already exist
   - Verify role names match exactly

### **Manual Recovery**
If the patch fails, you can run the setup manually:
```python
# In Frappe console
from tenantx.tenantx.setup_roles import run_full_setup
run_full_setup()
```

### **Disable Test Users**
To disable test user creation:
```python
# In site_config.json
{
    "tenantx_create_test_users": false
}
```

## Best Practices

### **1. Test in Development**
Always test patches in development before production:
```bash
# Test in development
bench --site dev-site.com migrate

# Verify setup
bench --site dev-site.com console
```

### **2. Backup Before Migration**
```bash
# Backup before running patches
bench --site site.com backup
```

### **3. Monitor Logs**
```bash
# Monitor patch execution
bench --site site.com tail-logs
```

### **4. Production Configuration**
For production environments:
```python
# site_config.json
{
    "tenantx_create_test_users": false,
    "tenantx_fail_on_error": true,
    "tenantx_detailed_logging": false
}
```

## Migration Commands

### **Run Migration with Patches**
```bash
# Migrate with automatic patch execution
bench --site site.com migrate

# Force patch execution
bench --site site.com execute tenantx.tenantx.patches.v1_0_0_setup_roles_and_permissions.execute
```

### **Skip Patches (if needed)**
```bash
# Migrate without running patches
bench --site site.com migrate --skip-patches
```

## Integration with CI/CD

### **Automated Deployment**
The patch system integrates seamlessly with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Deploy to Production
  run: |
    bench --site production.com migrate
    # Patches run automatically during migration
```

### **Rollback Strategy**
If patches cause issues:
```bash
# Restore from backup
bench --site site.com restore backup-file.sql

# Or manually remove created items
bench --site site.com console
# Remove roles, permissions, test users manually
```

---

## Summary

The TenantX patch system provides:
- ✅ **Automatic setup** during migrations
- ✅ **Safe execution** with error handling
- ✅ **Configurable behavior** for different environments
- ✅ **Production-ready** with safety features
- ✅ **Easy verification** and troubleshooting

This ensures your permission system is always properly configured without manual intervention! 