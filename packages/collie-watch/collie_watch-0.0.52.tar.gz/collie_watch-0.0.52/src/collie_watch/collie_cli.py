# cli_tool.py
from supabase import create_client,Client
from .main_module import *
import argparse


ANON_URL,ANON_TOKEN = "https://acyzjlibhoowdqjrdmwu.supabase.co","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFjeXpqbGliaG9vd2RxanJkbXd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTMyNTI2MDgsImV4cCI6MjAwODgyODYwOH0.cSP7MaxuIZUknfp-_9srZyiOmQwokEdDXlyo4mci_S8"

def main():
    parser = argparse.ArgumentParser(description='Collie Watch CLI tool')
    parser.add_argument("dashboard_token",type=str,help="The token of your dashboard")
    parser.add_argument('--monitor', type=str, help='Monitor a directory on your dashboard')

    args = parser.parse_args()

    if args.monitor:
        supabase = create_client(ANON_URL,ANON_TOKEN)

        #check for dashboard
        data,count = supabase.from_("dashboards").select("*").eq("dashboard_token",args.dashboard_token).execute()
        if len(data[1]) == 0:
            print(f'Could not find any dashboards with token "{args.dashboard_token}".\nPlease provide a valid dashboard token!')
            return False
       
        CollieWatch.initialize(args.dashboard_token,program_name="Collie Watch CLI Tool | Monitor")

        CollieWatch.create_block("File Browser")
        CollieWatch.set_text_on_block("File Browser","")
        

    

if __name__ == "__main__":
    main()
