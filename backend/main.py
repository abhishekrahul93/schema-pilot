import os
import sys
import subprocess

def print_banner():
    print('=' * 60)
    print('🚀 SCHEMAPILOT - Autonomous Analytics & Governance Engine')
    print('=' * 60)

def main():
    while True:
        print_banner()
        print('Select an option:')
        print('1. Run Multi-Agent SQL Query (Architect -> Coder -> Critic)')
        print('2. Run Audited Workflow with Telemetry Logging')
        print('3. Run Autonomous Auto-Coder & Self-Debugging Agent')
        print('4. Launch FastAPI Web Server')
        print('5. Exit')
        
        choice = input('\nEnter your choice (1-5): ').strip()
        
        if choice == '1':
            print('\n--- Running Multi-Agent Healing Workflow ---')
            subprocess.run([sys.executable, 'multi_agent_healing.py'])
        elif choice == '2':
            print('\n--- Running Audited Telemetry Workflow ---')
            subprocess.run([sys.executable, 'multi_agent_audited.py'])
        elif choice == '3':
            print('\n--- Running Auto-Coder Agent ---')
            subprocess.run([sys.executable, 'auto_coder_agent.py'])
        elif choice == '4':
            print('\n--- Starting FastAPI Web Server ---')
            print('Server will run at http://127.0.0.1:8000 (Press Ctrl+C to stop)')
            subprocess.run([sys.executable, '-m', 'uvicorn', 'app.main:app', '--reload'])
        elif choice == '5':
            print('\nExiting SchemaPilot. Goodbye! 👋')
            break
        else:
            print('❌ Invalid choice. Please enter a number between 1 and 5.')
        
        input('\nPress Enter to return to the main menu...')

if __name__ == '__main__':
    main()
