import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_pdf_document(filename, title, content):
    """Create a PDF document with the given title and content."""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    story = []
    
    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))
    
    # Add content paragraphs
    for paragraph in content.split('\n\n'):
        if paragraph.strip():
            story.append(Paragraph(paragraph.strip(), styles['Normal']))
            story.append(Spacer(1, 12))
    
    doc.build(story)
    print(f"Created: {filename}")

def main():
    # Create documents directory
    os.makedirs("documents", exist_ok=True)
    
    documents = {
        "employee_badge_request.pdf": {
            "title": "Employee Badge Request Process",
            "content": """To request a new employee badge or replace a lost/damaged badge, follow these steps:

1. Log into the Employee Portal at portal.company.com
2. Navigate to Security > Badge Requests
3. Select the type of request:
   - New Employee Badge
   - Replacement Badge (lost/stolen)
   - Replacement Badge (damaged)
4. Fill out the required information including:
   - Full name as it should appear on badge
   - Department and manager information
   - Access level required
   - Photo upload (passport-style, recent)
5. Submit the request for manager approval

Processing time is typically 3-5 business days after approval. You will receive an email notification when your badge is ready for pickup at the Security Office (Building A, Ground Floor).

For urgent requests, contact Security directly at ext. 2100 or security@company.com.

Badge pickup hours: Monday-Friday, 8:00 AM - 5:00 PM. Bring a valid government-issued photo ID for verification."""
        },
        
        "wifi_setup_guide.pdf": {
            "title": "WiFi Connection Setup Guide",
            "content": """Connect to the company WiFi network using these instructions:

Network Information:
- Network Name (SSID): CompanyWiFi
- Security Type: WPA2-Enterprise
- Authentication: Username/Password

Setup Instructions:

Windows:
1. Click the WiFi icon in the system tray
2. Select 'CompanyWiFi' from available networks
3. Enter your company username and password
4. If prompted for certificate, click 'Connect anyway'

Mac:
1. Click WiFi icon in menu bar
2. Select 'CompanyWiFi'
3. Enter username and password when prompted
4. Click 'Join'

Mobile Devices:
1. Go to WiFi settings
2. Select 'CompanyWiFi'
3. Choose 'WPA2-Enterprise' if prompted
4. Enter company credentials

Troubleshooting:
- Ensure your account is active in the system
- Try forgetting and reconnecting to the network
- Contact IT Support at ext. 3000 if issues persist

Guest WiFi is available as 'CompanyGuest' with password 'Welcome2024' (changes monthly)."""
        },
        
        "it_support_tickets.pdf": {
            "title": "IT Support Ticket Creation Guide",
            "content": """Create IT support tickets for technical assistance using our ticketing system:

Access Methods:
1. Online Portal: support.company.com
2. Email: itsupport@company.com
3. Phone: ext. 3000 (urgent issues only)
4. Walk-in: IT Help Desk (Building B, 2nd Floor)

Ticket Creation Process:
1. Log into the support portal with your company credentials
2. Click 'Create New Ticket'
3. Select the appropriate category:
   - Hardware Issues
   - Software Problems
   - Network/Connectivity
   - Account Access
   - New Equipment Request
   - Other

4. Provide detailed information:
   - Clear description of the issue
   - Steps you've already tried
   - Error messages (exact text)
   - When the problem started
   - Business impact level

Priority Levels:
- Critical: System down, business stopped
- High: Major functionality impacted
- Medium: Minor functionality issues
- Low: Enhancement requests, questions

Response Times:
- Critical: 1 hour
- High: 4 hours
- Medium: 1 business day
- Low: 3 business days

Track your tickets online or via email notifications. Include ticket number in all communications."""
        },
        
        "vpn_setup_instructions.pdf": {
            "title": "VPN Setup Instructions",
            "content": """Set up VPN access for secure remote connections to company resources:

Prerequisites:
- Active company account
- VPN access approval from your manager
- Company-issued device or approved personal device

Download VPN Client:
1. Visit vpn.company.com
2. Log in with company credentials
3. Download the appropriate client for your operating system
4. Install following the setup wizard

Configuration:
- Server Address: vpn.company.com
- Username: Your company username
- Password: Your company password
- Protocol: OpenVPN (recommended) or IKEv2

Connection Steps:
1. Launch VPN client
2. Enter server address if not pre-configured
3. Input your company credentials
4. Click Connect
5. Verify connection with green status indicator

Troubleshooting:
- Ensure stable internet connection
- Check firewall settings (allow VPN client)
- Try different server locations if available
- Restart VPN client and try again
- Contact IT if authentication fails

Security Notes:
- Always disconnect when not needed
- Never share VPN credentials
- Report suspicious activity immediately
- Use only for business purposes

For mobile devices, download the company VPN app from your device's app store and use the same credentials."""
        },
        
        "expense_reports.pdf": {
            "title": "Expense Report Submission Process",
            "content": """Submit expense reports for business-related expenses using our online system:

Accessing the System:
1. Go to expenses.company.com
2. Log in with company credentials
3. Click 'New Expense Report'

Eligible Expenses:
- Business travel (flights, hotels, meals)
- Client entertainment
- Office supplies
- Professional development
- Mileage for business use
- Conference and training fees

Required Documentation:
- Original receipts (digital photos acceptable)
- Business purpose description
- Date and location of expense
- Attendees for meals/entertainment
- Mileage logs with start/end locations

Submission Process:
1. Create new expense report
2. Add expense line items with details
3. Upload receipt images
4. Assign to appropriate cost center/project
5. Add business justification
6. Submit for manager approval

Approval Workflow:
1. Manager review and approval
2. Finance department verification
3. Payment processing (5-7 business days)

Important Guidelines:
- Submit within 30 days of expense
- Alcohol requires special approval
- Personal expenses are not reimbursable
- Keep copies of all documentation
- Maximum meal amounts vary by location

Reimbursement is via direct deposit to your registered bank account. Check status online or contact Finance at ext. 4000."""
        },
        
        "conference_room_booking.pdf": {
            "title": "Conference Room Booking System",
            "content": """Book conference rooms and meeting spaces using our reservation system:

Booking Methods:
1. Online Portal: rooms.company.com
2. Outlook/Calendar integration
3. Mobile app: Company Rooms
4. Reception desk (Building A)

Available Rooms:
- Small rooms (2-4 people): Rooms 101-110
- Medium rooms (5-8 people): Rooms 201-210  
- Large rooms (9-15 people): Rooms 301-305
- Auditorium (50+ people): Room 401
- Video conference rooms: Rooms VC1-VC5

Booking Process:
1. Log into the booking system
2. Select date and time
3. Choose room based on capacity needed
4. Add meeting title and description
5. Invite attendees
6. Confirm booking

Equipment Available:
- Projectors and screens
- Video conferencing systems
- Whiteboards and markers
- Conference phones
- Laptop connections (HDMI/USB-C)

Booking Rules:
- Maximum 4 hours per booking
- Book up to 30 days in advance
- Cancel if not needed (24hr notice preferred)
- No food/drinks except water
- Clean up after use

Special Requests:
- Catering setup: Contact facilities@company.com
- Technical support: ext. 3000
- After-hours access: Security approval required

Room access is via badge scan. Contact Reception at ext. 2000 for assistance or room issues."""
        },
        
        "time_off_requests.pdf": {
            "title": "Time Off Request Process",
            "content": """Request vacation, sick leave, and other time off through our HR system:

Types of Leave:
- Vacation/Personal Time Off (PTO)
- Sick Leave
- Personal Days
- Bereavement Leave
- Jury Duty
- Medical Leave (FMLA)

Request Process:
1. Log into HR Portal at hr.company.com
2. Navigate to Time Off > New Request
3. Select leave type and dates
4. Enter reason/notes if required
5. Submit for manager approval

Approval Requirements:
- Vacation: 2 weeks advance notice preferred
- Sick leave: As soon as possible
- Personal days: 1 week notice
- Extended leave: 30 days notice

Manager Approval:
- Requests go to direct manager first
- HR approval for extended leave
- Automatic approval for sick leave under 3 days
- Denial reasons provided if applicable

Important Policies:
- Minimum 4-hour increments
- Maximum 2 weeks consecutive vacation
- Blackout periods during busy seasons
- Unused PTO may carry over (check policy)
- Sick leave requires doctor's note after 3 days

Tracking:
- View balances in HR portal
- Receive email confirmations
- Calendar integration available
- Mobile app for quick requests

Emergency Leave:
- Call manager and HR immediately
- Submit request within 48 hours
- Documentation may be required
- Contact HR at ext. 5000 for urgent situations

Check your employee handbook for detailed leave policies and accrual rates."""
        },
        
        "new_employee_onboarding.pdf": {
            "title": "New Employee Onboarding Process",
            "content": """Welcome to the company! This guide covers your first week onboarding process:

Before Your Start Date:
- Complete background check and paperwork
- Receive welcome email with first-day instructions
- Set up direct deposit and benefits enrollment
- Review employee handbook

First Day Schedule:
9:00 AM - Check in at Reception (Building A)
9:30 AM - HR orientation and paperwork completion
11:00 AM - IT setup (laptop, accounts, access cards)
12:00 PM - Lunch with your manager
1:00 PM - Department introduction and workspace setup
3:00 PM - Benefits enrollment meeting
4:00 PM - Security briefing and badge photo

Week 1 Activities:
- Complete mandatory training modules
- Meet with key team members
- Review job responsibilities and goals
- Set up workspace and equipment
- Attend department meetings

Required Training (complete within 30 days):
- Information Security Awareness
- Workplace Safety
- Code of Conduct
- Diversity and Inclusion
- Emergency Procedures

IT Setup Includes:
- Company laptop and peripherals
- Email account and calendar access
- Software installations
- VPN and network access
- Phone system setup

Important Contacts:
- HR: ext. 5000 or hr@company.com
- IT Support: ext. 3000
- Security: ext. 2100
- Your Manager: [provided separately]
- Buddy/Mentor: [assigned on first day]

30-Day Check-in:
- Meeting with HR and manager
- Training completion verification
- Feedback and questions session
- Goal setting for next 90 days

Remember: Don't hesitate to ask questions! Everyone is here to help you succeed."""
        },
        
        "password_reset_guide.pdf": {
            "title": "Password Reset Procedures",
            "content": """Reset your company password using these self-service and support options:

Self-Service Password Reset:
1. Go to password.company.com
2. Enter your username
3. Choose verification method:
   - Security questions
   - SMS to registered phone
   - Email to alternate address
4. Follow verification steps
5. Create new password meeting requirements

Password Requirements:
- Minimum 12 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character (!@#$%^&*)
- Cannot reuse last 12 passwords
- Must change every 90 days

Alternative Reset Methods:
- Call IT Help Desk: ext. 3000
- Visit IT in person (Building B, 2nd Floor)
- Email: passwordreset@company.com
- Emergency after-hours: Security at ext. 2100

Account Lockout:
- Accounts lock after 5 failed attempts
- Automatic unlock after 30 minutes
- Contact IT for immediate unlock
- Lockout notifications sent to manager

Security Best Practices:
- Use unique passwords for each account
- Enable two-factor authentication
- Never share passwords
- Use password manager if approved
- Report suspicious activity immediately

Forgot Username:
- Contact IT Support with employee ID
- Provide verification information
- Username reminder sent to registered email

Two-Factor Authentication:
- Required for all accounts
- Use company-approved authenticator app
- Backup codes provided during setup
- Contact IT if device is lost/replaced

If you suspect your password has been compromised, change it immediately and report to IT Security at security@company.com."""
        },
        
        "remote_work_policy.pdf": {
            "title": "Remote Work Policy and Guidelines",
            "content": """Guidelines for employees working remotely or in hybrid arrangements:

Eligibility:
- Full-time employees after 90-day probation
- Manager approval required
- Role must be suitable for remote work
- Demonstrated ability to work independently

Work Arrangements:
- Fully remote: 5 days per week from home
- Hybrid: 2-3 days remote, remainder in office
- Flexible: Varies based on business needs
- Temporary remote: Short-term arrangements

Equipment and Technology:
- Company laptop and necessary peripherals
- VPN access for secure connections
- Video conferencing software
- Cloud-based collaboration tools
- Ergonomic home office setup (reimbursable)

Home Office Requirements:
- Dedicated workspace
- Reliable high-speed internet
- Quiet environment for calls
- Proper lighting for video calls
- Secure storage for company materials

Communication Expectations:
- Available during core hours (9 AM - 3 PM)
- Respond to messages within 4 hours
- Participate in video calls with camera on
- Use status indicators in messaging apps
- Regular check-ins with manager

Performance Standards:
- Same productivity expectations as office work
- Clear goal setting and regular reviews
- Time tracking may be required
- Deliverable-based performance metrics

Security Requirements:
- Use only company-approved devices
- Secure home WiFi network
- Lock screen when away
- No public WiFi for sensitive work
- Report security incidents immediately

Expense Reimbursement:
- Internet costs (up to $50/month)
- Office furniture (up to $500 one-time)
- Office supplies as needed
- Submit receipts through expense system

This policy is subject to change based on business needs and may be revoked with 30 days notice."""
        }
    }
    
    # Create all PDF documents
    for filename, doc_info in documents.items():
        filepath = os.path.join("documents", filename)
        create_pdf_document(filepath, doc_info["title"], doc_info["content"])
    
    print(f"\nSuccessfully created {len(documents)} PDF documents in the 'documents' directory.")

if __name__ == "__main__":
    main()