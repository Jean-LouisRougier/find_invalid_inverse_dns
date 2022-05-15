import sys
from netaddr import IPNetwork
from dns import resolver,reversename
import subprocess, platform

def pingOk(sHost):
    try:
        output = subprocess.check_output("ping -{} 1 -W0.5 {}".format('n' if platform.system().lower()=="windows" else 'c', sHost), shell=True)

    except :
        return False

    return True


if (len(sys.argv)<2): 
    print("Usage: scan_invdns <prefix> (verbosity)")
    print("  Verbosity: quiet/q: only incoherent values (default)")
    print("             verbose/v: all")
    exit()
verbose=False
if len(sys.argv)==3:
    if sys.argv[2]=='verbose' or sys.argv[2]=='v':
        verbose=True
subnet=IPNetwork(str(sys.argv[1]))
print("Scanning:", subnet)
no_ptr=0
valid_ptr=0
unvalid_ptr=0
unverified_ptr=0
total=0
unused=0

for ip in IPNetwork(str(sys.argv[1])): 
    #print(ip)
    total+=1
    addr=reversename.from_address(str(ip))
    verif_ip=""
    #status=""
    try: 
        ans=resolver.resolve(addr,"PTR")
        try: 
            verif_ip=resolver.resolve(str(ans[0]), "A")
            #print("       DNS_A:",str(verif_ip[0]), "/", str(ip))
            if (str(verif_ip[0])==str(ip)):
                valid_ptr+=1
                #status+="/Valid_PTR"
                if verbose:
                    print(ip,":",ans[0]," (verified address)")
                
            else:
                unvalid_ptr+=1
                #status+="/Unvalid_PTR"
                print(ip,":",ans[0]," Incoherence found:",str(verif_ip[0]))

        except:
            unverified_ptr+=1
            #status+="/Unverified_PTR"
            if verbose==True:
                print(ip,":",ans[0], " (unverified, DNS failed)")
            
    except:
        if pingOk(ip):
            no_ptr+=1
            #status+="/Unused_IP"
            if verbose==True:
                print(ip, ": Unused (no PTR, no Ping)")
        else:
            unused+=1
            #status+="/No_PTR"
            if verbose==True:
                print(ip, ": no PTR found")

    #print("Variables:",no_ptr," ",valid_ptr," ", unvalid_ptr," ", unverified_ptr, " ", unused )
    #print("Status:", status)
print("")
print("*** Summary ***")
print(total," addresses scanned")
print("No PTR         ", 100.0*no_ptr/total, "%")
print("Valid PTR      ", 100.0*valid_ptr/total, "%")
print("Unvalid PTR    ", 100.0*unvalid_ptr/total, "%")
print("Unverified PTR ", 100.0*unverified_ptr/total, "%")
print("Unused         ", 100.0*unused/total, "%")





