# Changelog - Security Testing Framework

## Version 2.0 - Advanced Edition

### New Features

#### ✅ Module DeAPoL (Deep Packet Layer)
- Network packet injection for opening phishing pages on target devices
- Real ARP scanning using Scapy
- Multiple attack vectors (HTTP injection, DNS poisoning, ARP spoofing)
- Device discovery with IP, MAC, and status
- Stealth and persistent modes

#### ✅ Module OSINT Intelligence
- Email target enumeration
- Domain information gathering (WHOIS lookup)
- DNS record analysis (A, MX records)
- Email breach checking via Have I Been Pwned
- Social media discovery
- Results export functionality

#### ✅ Module Email Campaign
- Send phishing emails with HTML templates
- Generate fake email addresses automatically
- SMTP server configuration
- Real email sending (no simulation)
- Activity logging to files
- Template customization

#### ✅ SEToolkit Advanced Module
- Credential Harvester Attack
- Java Applet Attack
- USB HID Attack
- Web Jacking Attack
- Mass Mailer Attack
- SMS Spoofing Attack
- Wireless Access Point creation

### Technical Improvements

#### Removed Simulations
- All modules now use real implementations
- No more `time.sleep()` placeholders
- Actual network scanning with Scapy
- Real SMTP email sending
- Real DNS and WHOIS lookups

#### Enhanced Phishing Module
- Real Flask server integration
- Template serving on target IPs
- Automatic data capture and logging
- Customizable redirect URLs
- Professional HTML templates

#### Better Architecture
- Threading for async operations
- Proper error handling
- Logging infrastructure
- Modular design
- English interface throughout

### Dependencies Added
- `scapy==2.5.0` - Packet manipulation
- `python-whois==0.8.0` - Domain information
- `dnspython==2.4.2` - DNS queries
- `Flask==3.0.0` - Web server

### Security Enhancements
- Warning messages throughout UI
- Legal disclaimer on main page
- Proper error handling
- Safe defaults

## Version 1.0 - Initial Release

### Core Features
- Basic phishing module
- Cloning module
- Reconnaissance module
- Payload generator
- Web attack module
- PyQt5 GUI

---

**Note**: Always use responsibly and only on authorized systems.

