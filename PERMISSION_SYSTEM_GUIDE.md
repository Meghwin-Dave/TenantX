# Permission System Guide for TenantX

## Overview

The TenantX app implements a comprehensive permission system that controls user access to Factory Business Units (FBUs), Strategic Business Units (SBUs), and related transactional documents based on cost center associations.

## How It Works

### 1. Direct Document Permissions

Users can be granted direct access to:
- **Factory Business Unit**: Users can see and manage specific factories
- **Strategic Business Unit**: Users can see and manage specific SBUs
- **Cost Center**: Users can see and manage specific cost centers

### 2. Transactional Document Permissions

For transactional documents (Purchase Orders, Sales Invoices, etc.), the system checks if the document's cost center is linked to:
- A Factory Business Unit the user has access to
- A Strategic Business Unit the user has access to
- A Cost Center the user has direct access to

### 3. Permission Query Functions

The system uses `get_permission_query_conditions` functions to filter data based on user permissions:

#### For Direct Documents:
- `Factory Business Unit`: `tenantx.tenantx.doctype.factory_business_unit.factory_business_unit.get_permission_query_conditions`
- `Strategic Business Unit`: `tenantx.tenantx.doctype.strategic_business_unit.strategic_business_unit.get_permission_query_conditions`

#### For Transactional Documents:
- `Purchase Order`: `tenantx.tenantx.permission_queries.get_permission_query_conditions_for_purchase_order`
- `Sales Invoice`: `tenantx.tenantx.permission_queries.get_permission_query_conditions_for_sales_invoice`
- `Purchase Invoice`: `tenantx.tenantx.permission_queries.get_permission_query_conditions_for_purchase_invoice`
- `Sales Order`: `tenantx.tenantx.permission_queries.get_permission_query_conditions_for_sales_order`
- `Delivery Note`: `tenantx.tenantx.permission_queries.get_permission_query_conditions_for_delivery_note`
- `Purchase Receipt`: `tenantx.tenantx.permission_queries.get_permission_query_conditions_for_purchase_receipt`
- `Journal Entry`: `tenantx.tenantx.permission_queries.get_permission_query_conditions_for_journal_entry`

## Permission Logic

### System Manager Access
- System Managers have full access to all documents
- No permission restrictions apply

### Regular User Access
The system checks for user permissions in this order:

1. **Direct Factory Business Unit Access**: User has User Permission for specific FBUs
2. **Direct Strategic Business Unit Access**: User has User Permission for specific SBUs  
3. **Direct Cost Center Access**: User has User Permission for specific Cost Centers
4. **Indirect Access via Cost Centers**: User can access documents where the cost center is linked to their allowed FBUs/SBUs

### Permission Query Logic

For each document type, the system:

1. Gets the user's allowed Factory Business Units from User Permissions
2. Gets the user's allowed Strategic Business Units from User Permissions
3. Gets the user's directly allowed Cost Centers from User Permissions
4. Builds SQL conditions to check if the document's cost center matches any of the allowed entities
5. Returns a SQL WHERE clause that filters documents accordingly

## Implementation Details

### Files Modified

1. **`apps/tenantx/tenantx/tenantx/doctype/factory_business_unit/factory_business_unit.py`**
   - Added `get_permission_query_conditions` function

2. **`apps/tenantx/tenantx/tenantx/doctype/strategic_business_unit/strategic_business_unit.py`**
   - Added `get_permission_query_conditions` function

3. **`apps/tenantx/tenantx/tenantx/permission_queries.py`** (New File)
   - Contains permission query functions for all transactional documents

4. **`apps/tenantx/tenantx/hooks.py`**
   - Registered all permission query functions in `permission_query_conditions`

### SQL Query Examples

#### Factory Business Unit Permission Query:
```sql
(`tabFactory Business Unit`.`name` IN (
    SELECT `for_value` FROM `tabUser Permission`
    WHERE `user`='user@example.com' AND `allow`='Factory Business Unit'
))
```

#### Transactional Document Permission Query:
```sql
(`tabPurchase Order`.`cost_center` IN (
    SELECT `cost_center` FROM `tabFactory Business Unit`
    WHERE `name` IN ('FACTORY-001', 'FACTORY-002')
)) OR (`tabPurchase Order`.`cost_center` IN (
    SELECT `cost_center` FROM `tabStrategic Business Unit`
    WHERE `name` IN ('SBU-001', 'SBU-002')
)) OR (`tabPurchase Order`.`cost_center` IN ('CC-001', 'CC-002'))
```

## Usage Instructions

### Setting Up User Permissions

1. **For Factory Business Units:**
   - Go to User Permissions
   - Add permission for user
   - Select "Factory Business Unit" as the document type
   - Choose specific Factory Business Units

2. **For Strategic Business Units:**
   - Go to User Permissions
   - Add permission for user
   - Select "Strategic Business Unit" as the document type
   - Choose specific Strategic Business Units

3. **For Cost Centers:**
   - Go to User Permissions
   - Add permission for user
   - Select "Cost Center" as the document type
   - Choose specific Cost Centers

### Testing Permissions

1. **Login as a regular user** (not System Manager)
2. **Navigate to any of the protected document types**
3. **Verify that only documents with allowed cost centers are visible**
4. **Check that the user cannot see documents outside their scope**

## Security Considerations

1. **System Manager Override**: System Managers always have full access
2. **No Permission = No Access**: Users without any permissions see no documents
3. **Cost Center Linking**: All permissions are enforced through cost center associations
4. **SQL Injection Protection**: All queries use parameterized queries for security

## Troubleshooting

### Common Issues

1. **User sees no documents:**
   - Check if user has any User Permissions set up
   - Verify that the cost centers in documents are linked to allowed FBUs/SBUs

2. **User sees too many documents:**
   - Check if user has System Manager role
   - Verify User Permissions are correctly configured

3. **Permission queries not working:**
   - Ensure hooks.py is properly configured
   - Check that all permission query functions are correctly implemented
   - Verify that cost centers are properly linked to FBUs/SBUs

### Debugging

To debug permission issues:

1. **Check User Permissions:**
   ```python
   frappe.db.sql("""
       SELECT * FROM `tabUser Permission`
       WHERE `user` = 'user@example.com'
   """)
   ```

2. **Check Cost Center Associations:**
   ```python
   frappe.db.sql("""
       SELECT name, cost_center FROM `tabFactory Business Unit`
       WHERE cost_center IS NOT NULL
   """)
   ```

3. **Test Permission Query:**
   ```python
   from tenantx.tenantx.permission_queries import get_permission_query_conditions_for_purchase_order
   condition = get_permission_query_conditions_for_purchase_order('user@example.com')
   print(condition)
   ```

## Future Enhancements

1. **Role-based Permissions**: Add role-based permission system
2. **Hierarchical Permissions**: Support for parent-child permission inheritance
3. **Time-based Permissions**: Add time restrictions to permissions
4. **Audit Trail**: Track permission changes and access logs
5. **Bulk Permission Management**: Tools for managing permissions in bulk 