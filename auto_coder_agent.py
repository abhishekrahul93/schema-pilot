import os
import sys
import subprocess
import duckdb
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def run_auto_coder(task_description: str):
    print(f'\n🚀 [Auto-Coder Agent] Task: \'{task_description}\'')
    print('=' * 60)
    prompt = 'You are an Expert Autonomous Python Data Engineer.\nWrite a complete, executable Python script to accomplish this task using DuckDB (\'schemapilot.duckdb\').\nThe script must use sys.executable or ensure the correct environment, and print the final results cleanly.\nOutput ONLY valid Python code inside a markdown code block (`python ... `).\nTask: ' + task_description
    print('💻 [Agent] Generating Python code...')
    response = client.chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'user', 'content': prompt}], temperature=0)
    raw_content = response.choices[0].message.content
    code = raw_content.split('`python')[1].split('`')[0].strip() if '`python' in raw_content else (raw_content.split('`')[1].split('`')[0].strip() if '`' in raw_content else raw_content.strip())
    
    python_executable = sys.executable
    for attempt in range(1, 4):
        print(f'\n⚙️ [Execution Attempt {attempt}/3] Running generated script...')
        try:
            with open('temp_generated_script.py', 'w', encoding='utf-8') as sf:
                sf.write(code)
            res = subprocess.run([python_executable, 'temp_generated_script.py'], capture_output=True, text=True, timeout=15)
            if res.returncode != 0:
                raise RuntimeError(res.stderr)
            print('✅ Code Executed Successfully!\n📊 Output:\n' + res.stdout)
            break
        except Exception as e:
            print(f'⚠️ [Auto-Repair] Error caught:\n{e}')
            if attempt == 3:
                print('❌ Max retries reached.')
                break
            fix_res = client.chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'user', 'content': f'Fix this failed Python script error: {e}. Task: {task_description}. Failed Code:\n{code}\nOutput ONLY valid Python code inside a markdown block.'}], temperature=0)
            fixed = fix_res.choices[0].message.content
            code = fixed.split('`python')[1].split('`')[0].strip() if '`python' in fixed else fixed.strip()
    if os.path.exists('temp_generated_script.py'):
        os.remove('temp_generated_script.py')
    print('\n✨ Auto-Coder Workflow Complete!')

if __name__ == '__main__':
    run_auto_coder('Query the fct_orders table in schemapilot.duckdb, find the top 2 countries by total quantity, and print the results.')
