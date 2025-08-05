# TenantX

A comprehensive Frappe/ERPNext application for managing multi-level companies, enterprises, and warehouses with hierarchical organizational structures and advanced access control.

## Overview

TenantX provides a robust framework for managing complex organizational hierarchies including enterprises, strategic business units (SBUs), factories, and liaison offices. It's designed to handle multi-tenant scenarios with ease, offering granular control over business operations, financial management, and user access control.

## 🚀 Key Features

### 🏢 **Enterprise Management**
- **Multi-level Enterprise Hierarchy**: Parent-child relationships with unlimited nesting levels
- **Enterprise Type Categorization**: Flexible categorization system for different business types
- **Separate Entity Management**: Support for both group and separate entity enterprises
- **Tax ID and Contact Information**: Comprehensive tracking of legal and contact details
- **Active/Inactive Status Management**: Granular control over enterprise status
- **Cost Center Integration**: Automatic cost center creation and management
- **Company Association**: Direct linking with ERPNext companies

### 🎯 **Strategic Business Units (SBUs)**
- **SBU Creation and Management**: Strategic divisions within enterprises
- **Business Segment Association**: Link SBUs to specific business segments
- **Factory Business Unit Linking**: Connect SBUs to multiple factories
- **Cost Center Integration**: Financial tracking and reporting
- **SBU Head Assignment**: Employee-based leadership management
- **Hierarchical SBU Structure**: Parent-child SBU relationships
- **Multi-Factory Association**: Link multiple factories to a single SBU

### 🏭 **Factory Business Units**
- **Factory Categorization**: Type-based factory classification
- **Capacity Management**: Track production capacity with UOM support
- **Warehouse Integration**: Direct warehouse association and management
- **Factory Head Assignment**: Employee-based factory leadership
- **Customer Association**: Link factories to specific customers
- **Contact and Address Management**: Complete location and contact tracking
- **Cost Center Management**: Financial tracking for factory operations

### 🌍 **Liaison Offices**
- **International Office Management**: Global office representation
- **Country-based Organization**: Geographic organization structure
- **Liaison Head Assignment**: Employee-based office leadership
- **Contact and Address Management**: Complete contact information tracking

### 📊 **Business Segments**
- **Business Segment Categorization**: Industry and market segment classification
- **Description and Documentation**: Detailed segment information
- **Hierarchical Organization Support**: Multi-level segment structure

### 🔐 **Access Control & Security**
- **SBU Access Control**: Granular access management for SBUs
  - Full Access: Complete control over SBU operations
  - Limited Access: Restricted operational permissions
  - View Only: Read-only access to SBU data
- **Factory Access Control**: Detailed factory-level access management
  - Primary Factory Access: Main operational control
  - Secondary Factory Access: Supporting operational access
  - Backup Factory Access: Emergency access capabilities
- **User Role Management**: Custom role definitions for TenantX
- **Approval Workflows**: Factory association approval processes

### 📋 **Master Data Management**
- **Enterprise Types**: Configurable enterprise categorization
- **Factory Categories**: Flexible factory type classification
- **Business Segments**: Industry and market segment definitions
- **Naming Series**: Configurable naming conventions for all entities

### 🔗 **Integration Features**
- **ERPNext Integration**: Seamless integration with ERPNext modules
- **Company Linking**: Direct association with ERPNext companies
- **Cost Center Management**: Automatic cost center creation and linking
- **Employee Integration**: Direct linking with employee records
- **Warehouse Management**: Integration with ERPNext warehouse system
- **Customer Management**: Customer association and tracking
- **Contact & Address Integration**: Full integration with ERPNext contact system

## 📋 DocTypes

### 1. **Enterprise** - Core Organizational Unit
**Key Features:**
- Enterprise Name & Code with validation
- Enterprise Type categorization
- Parent Enterprise for hierarchical structure
- Company association
- Tax ID with format validation
- Is Group / Is Separate Entity flags
- Contact & Address information
- Cost Center integration
- Active/Inactive status management

**Naming Series:** `ENT-.#####`

**Validation Rules:**
- Enterprise code must be alphanumeric (uppercase, numbers, hyphens, underscores)
- Minimum 3 characters length
- Unique across all enterprises
- Tax ID format validation (5-20 characters, alphanumeric)
- Parent enterprise must be active and marked as group
- Prevents circular references

### 2. **Enterprise Type** - Master Data
**Key Features:**
- Enterprise Type name
- Description field
- Configurable categorization

**Naming Series:** `ENTT-.#####`

### 3. **Strategic Business Unit (SBU)** - Strategic Divisions
**Key Features:**
- SBU Name & Code
- Company & Enterprise association
- Factory Business Unit linking (multiple)
- Business Segment association
- SBU Head (Employee)
- Cost Center integration
- Parent SBU for hierarchy
- Active/Inactive status
- Description field

**Naming Series:** `SBU-.#####`

### 4. **Business Segment** - Market Segmentation
**Key Features:**
- Segment Name
- Description field
- Industry categorization

**Naming Series:** `BS-.#####`

### 5. **Factory Business Unit** - Physical Operations
**Key Features:**
- Factory Name & Code
- Company & Enterprise association
- SBU linking
- Factory Category
- Capacity & Capacity UOM
- Warehouse association
- Factory Head (Employee)
- Cost Center integration
- Contact & Address information
- Customer Details (table)
- Warehouse Details (table)
- Active/Inactive status

**Naming Series:** `FBU-.#####`

### 6. **Factory Category** - Factory Classification
**Key Features:**
- Factory Category name
- Description field
- Type-based categorization

**Naming Series:** `FC-.#####`

### 7. **Liaison Office** - International Offices
**Key Features:**
- Office Name & Code
- Enterprise association
- Country selection
- Liaison Head (Employee)
- Contact & Address information

**Naming Series:** `LO-.#####`

### 8. **Access Control DocTypes**

#### **SBU Access** - SBU Level Access Control
**Key Features:**
- SBU association
- Access Type (Full/Limited/View Only)
- Primary access designation
- User-based access management

#### **Factory Access** - Factory Level Access Control
**Key Features:**
- Factory association
- Access Type (Full/Limited/View Only)
- Primary access designation
- Granular factory permissions

#### **Factory Association** - Factory Relationships
**Key Features:**
- Factory linking
- Association Type (Primary/Secondary/Backup)
- Approval workflow support
- Multi-factory relationships

### 9. **Detail DocTypes**

#### **Customer Details** - Customer Association
**Key Features:**
- Customer linking
- Customer name auto-fetch
- Customer group information
- Factory-customer relationships

#### **Warehouse Details** - Warehouse Management
**Key Features:**
- Warehouse linking
- Parent warehouse information
- Account association
- Factory-warehouse relationships

#### **FBU List** - Factory Business Unit Lists
**Key Features:**
- Factory Business Unit linking
- Multi-select functionality
- SBU-factory relationships

## 🛠️ Installation

### Prerequisites
- Frappe Framework (v14+)
- ERPNext (recommended)
- Bench CLI
- Python 3.10+

### Installation Steps

1. **Clone the repository:**
```bash
cd $PATH_TO_YOUR_BENCH
bench get-app tenantx --branch develop
```

2. **Install the app:**
```bash
bench install-app tenantx
```

3. **Migrate the database:**
```bash
bench migrate
```

## 📖 Usage Guide

### Setting Up Your Organization

1. **Create Enterprise Types**
   - Navigate to TenantX > Enterprise Type
   - Create types like "Manufacturing", "Trading", "Service", "Holding Company", etc.

2. **Create Business Segments**
   - Navigate to TenantX > Business Segment
   - Create segments like "Electronics", "Automotive", "Healthcare", "Retail", etc.

3. **Create Factory Categories**
   - Navigate to TenantX > Factory Category
   - Create categories like "Assembly", "Processing", "Packaging", "Testing", etc.

4. **Create Enterprises**
   - Navigate to TenantX > Enterprise
   - Create your main enterprise with appropriate type
   - Set up parent-child relationships for complex hierarchies
   - Configure cost centers if needed

5. **Create Strategic Business Units**
   - Navigate to TenantX > Strategic Business Unit
   - Associate with enterprises and business segments
   - Assign SBU heads and cost centers
   - Link to factory business units

6. **Create Factory Business Units**
   - Navigate to TenantX > Factory Business Unit
   - Link to enterprises, SBUs, and warehouses
   - Set capacity and assign factory heads
   - Associate customers and warehouses

7. **Create Liaison Offices**
   - Navigate to TenantX > Liaison Office
   - Set up international offices with country information
   - Assign liaison heads

8. **Configure Access Control**
   - Set up SBU access for users
   - Configure factory access permissions
   - Establish factory associations

### Hierarchical Structure Example

```
Enterprise (Parent - Manufacturing)
├── Enterprise Type: Manufacturing
├── Strategic Business Unit 1 (Electronics Division)
│   ├── Business Segment: Electronics
│   ├── SBU Head: John Doe
│   └── Factory Business Unit 1 (Main Assembly)
│       ├── Factory Category: Assembly
│       ├── Capacity: 1000 units/day
│       ├── Factory Head: Jane Smith
│       ├── Warehouse: Main Warehouse
│       └── Customers: TechCorp, InnovateInc
├── Strategic Business Unit 2 (Automotive Division)
│   ├── Business Segment: Automotive
│   ├── SBU Head: Mike Johnson
│   └── Factory Business Unit 2 (Processing Plant)
│       ├── Factory Category: Processing
│       ├── Capacity: 500 units/day
│       ├── Factory Head: Sarah Wilson
│       ├── Warehouse: Secondary Warehouse
│       └── Customers: AutoMax, CarTech
└── Liaison Office (US Operations)
    ├── Country: United States
    ├── Liaison Head: Tom Brown
    └── Address: New York, NY
```

## ⚙️ Configuration

### Permissions
All doctypes are configured with System Manager permissions by default. You can customize permissions based on your organizational needs through:
- Role-based access control
- User-specific permissions
- SBU and Factory access management

### Naming Series
Each doctype uses configurable naming series for easy identification:
- Enterprise: `ENT-.#####`
- Enterprise Type: `ENTT-.#####`
- SBU: `SBU-.#####`
- Business Segment: `BS-.#####`
- Factory Business Unit: `FBU-.#####`
- Factory Category: `FC-.#####`
- Liaison Office: `LO-.#####`

### Access Control Levels
- **Full Access**: Complete control over operations, data, and settings
- **Limited Access**: Restricted operational permissions, read-write access to specific areas
- **View Only**: Read-only access to data and reports

## 🔧 Development

### Code Quality Standards
- **Python**: Follows PEP 8 standards with ruff linting
- **JavaScript**: ESLint configuration with prettier formatting
- **Pre-commit Hooks**: Automatic code formatting and linting
- **Type Annotations**: Python type hints for better code documentation

### Testing
Each doctype includes comprehensive test files. Run tests using:
```bash
bench run-tests --app tenantx
```

### Development Setup
This app uses `pre-commit` for code formatting and linting. Install and enable it:
```bash
cd apps/tenantx
pre-commit install
```

**Pre-commit Tools:**
- ruff (Python linting and formatting)
- eslint (JavaScript linting)
- prettier (JavaScript formatting)
- pyupgrade (Python code modernization)

## 📊 Business Benefits

### **Organizational Clarity**
- Clear hierarchical structure visualization
- Defined roles and responsibilities
- Streamlined reporting relationships

### **Operational Efficiency**
- Centralized enterprise management
- Automated cost center creation
- Integrated warehouse and customer management

### **Financial Control**
- Cost center integration for financial tracking
- Multi-level financial reporting
- Budget allocation and monitoring

### **Access Management**
- Granular user access control
- Role-based permissions
- Secure data access

### **Scalability**
- Support for unlimited organizational levels
- Flexible categorization systems
- Multi-tenant architecture

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code quality
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Write comprehensive tests
- Update documentation for new features

## 📄 License

MIT License - see [license.txt](license.txt) for details.

## 🆘 Support

For support and questions:
- **Email**: meghwin@cognitionx.tech
- **Publisher**: CognitionXLogic
- **Documentation**: See inline code documentation

## 📈 Version History

### **v1.0.0** - Initial Release
- ✅ Enterprise hierarchy management
- ✅ SBU and Factory Business Unit support
- ✅ Liaison office management
- ✅ Business segment categorization
- ✅ Factory category management
- ✅ Access control system
- ✅ Cost center integration
- ✅ Customer and warehouse association
- ✅ Comprehensive validation rules
- ✅ Multi-level organizational support

---

**TenantX** - Manage multi-level companies and warehouses with super ease

*Built with ❤️ by CognitionXLogic*
