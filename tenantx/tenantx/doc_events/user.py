import frappe
from frappe import _

def on_update(doc, method):
    """
    Update User Permissions based on user_access_scope child table
    This function implements Phase 2 of the permission system roadmap
    """
    try:
        update_user_permissions(doc, method)
    except Exception as e:
        frappe.logger().error(f"Error updating user permissions for {doc.name}: {str(e)}")
        frappe.throw(_("Failed to update user permissions: {0}").format(str(e)))


def update_user_permissions(doc, method):
    """
    Automate User Permission creation based on user_access_scope
    This implements the data-driven permission approach
    """
    # Delete existing permissions for TenantX document types
    allowed_doctypes = ["Enterprise", "Strategic Business Unit", "Factory Business Unit", "Liaison Office"]
    
    frappe.db.delete("User Permission", {
        "user": doc.name,
        "allow": ["in", allowed_doctypes]
    })
    
    # Commit the deletion to avoid any conflicts
    frappe.db.commit()
    
    # Create new permissions from the child table
    user_access_scope = doc.get("user_access_scope") or []
    
    for scope in user_access_scope:
        if scope.scope_type and scope.scope_name:
            # Validate the scope assignment
            if not frappe.db.exists(scope.scope_type, scope.scope_name):
                frappe.logger().warning(f"Scope document {scope.scope_name} does not exist in {scope.scope_type}")
                continue
            
            # Check if this permission already exists (extra safety)
            existing = frappe.db.exists("User Permission", {
                "user": doc.name,
                "allow": scope.scope_type,
                "for_value": scope.scope_name
            })
            
            if not existing:
                # Create the permission document
                permission_doc = frappe.get_doc({
                    "doctype": "User Permission",
                    "user": doc.name,
                    "allow": scope.scope_type,
                    "for_value": scope.scope_name,
                    "applicable_for": None,  # Set if you want to restrict to specific doctypes
                    "is_default": scope.is_primary if hasattr(scope, 'is_primary') else 0,
                })
                
                permission_doc.insert(ignore_permissions=True)
                
                frappe.logger().info(f"Created User Permission for {doc.name}: {scope.scope_type} - {scope.scope_name}")
    
    # Clear user permissions cache
    frappe.clear_cache(user=doc.name)


def create_hierarchical_permissions(user, scope_type, scope_name):
    """
    Create hierarchical permissions (Phase 4 enhancement)
    For example, if user has access to an SBU, they should also have access to all factories under that SBU
    """
    if scope_type == "Strategic Business Unit":
        # Find all factories under this SBU
        factories = frappe.db.sql_list("""
            SELECT name FROM `tabFactory Business Unit`
            WHERE sbu = %s AND is_active = 1
        """, scope_name)
        
        for factory in factories:
            # Create permission for each factory
            if not frappe.db.exists("User Permission", {
                "user": user,
                "allow": "Factory Business Unit",
                "for_value": factory
            }):
                frappe.get_doc({
                    "doctype": "User Permission",
                    "user": user,
                    "allow": "Factory Business Unit",
                    "for_value": factory,
                    "applicable_for": None,
                    "is_default": 0,
                }).insert(ignore_permissions=True)
    
    elif scope_type == "Enterprise":
        # Find all SBUs under this Enterprise
        sbus = frappe.db.sql_list("""
            SELECT name FROM `tabStrategic Business Unit`
            WHERE enterprise = %s AND is_active = 1
        """, scope_name)
        
        for sbu in sbus:
            # Create permission for each SBU
            if not frappe.db.exists("User Permission", {
                "user": user,
                "allow": "Strategic Business Unit",
                "for_value": sbu
            }):
                frappe.get_doc({
                    "doctype": "User Permission",
                    "user": user,
                    "allow": "Strategic Business Unit",
                    "for_value": sbu,
                    "applicable_for": None,
                    "is_default": 0,
                }).insert(ignore_permissions=True)
            
            # Also create permissions for factories under this SBU
            create_hierarchical_permissions(user, "Strategic Business Unit", sbu)
