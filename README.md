# find_invalid_inverse_dns
Scan a CIDR block with inverse DNS and find invalid entries

Usage: python3 scan_invdns.py <prefix> (verbosity)

Verbosity: 
           quiet/q: only incoherent values (default)
           verbose/v: info on each entry 
  

           
## Output: 
    
- No PTR: No entry found in Inverse DNS for this address (No PTR found)
- Valid PTR: IP address is associated with a domain name (PTR exists) and the domain name points back to the same IP address
- Unvalid PTR: IP address is associated with a domain name (PTR exists), however the domain name does not back to the same IP address...
- Unverified PTR: 
Example:
*** Summary ***
8192  addresses scanned
No PTR          36.9140625 %
Valid PTR       45.41015625 %
Unvalid PTR     4.94384765625 %
Unverified PTR  0.0 %
           
