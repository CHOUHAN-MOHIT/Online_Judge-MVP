import filecmp
import subprocess


def execute_code(code, input_data):
    try:
        # Save the code to a temporary file
        with open('temp_code.py', 'w') as file:
            file.write(code)

        # Run the code in a subprocess with input data
        process = subprocess.Popen(['python', 'temp_code.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=input_data.encode())

        # Check for any errors during code execution
        if process.returncode != 0:
            return False, stderr.decode()
        
        return True, stdout.decode()
    
    except Exception as e:
        return False, str(e)



def runcode(inputfile , generated_output ):
    subprocess.run(['g++' , 'temp.cpp' , '-o' , 'temp'])
    subprocess.run(['temp.exe'],input=inputfile ,stdout=generated_output,shell=True)

def get_verdict():
    result = filecmp.cmp('output.txt' , 'exp_out.txt' , shallow=False)
    if result:
        return 'AC'
    else:
        return 'WA'
    

def submit(request , pid):
    # fetch problem object using pid and then test with problem_name
    problem = Problem.objects.get(pk=pid)
    test = Test.objects.get(problem__problem_name=problem.problem_name)
    # checking method
    if request.method == 'POST':
        # fetching file and code submitted by user
        user_codefile = request.FILES.get('codeFile', False)
        codeInEditor = request.POST.get('codeEditor', False)
        # if user has submitted code through a file
        if user_codefile:
            # copy the content of codefile to temp.cpp
            codefile_content = user_codefile.read()
            with open('temp.cpp' , 'wb+') as temp_code:
                temp_code.write(codefile_content)
            temp_code.close()
            # open some useful files and write the desired content
            expout = open('exp_out.txt' , 'w')
            output = open('output.txt' , 'w')
            expout.write(test.test_output)
            input = bytes(test.test_input , 'utf-8')
            # get verdict
            verdict = evalueate(input, output)
            input.close()
            expout.close()
            # check for verdict
            if verdict:
                file =  open('temp.cpp')
                file = File(file)
                sol = Solution(
                    user = request.user,
                    problem=problem,
                    language=request.POST['language'],
                    code_file=file,
                    verdict='AC'
                )
                sol.save()
                file.close()
                return HttpResponseRedirect("/submit/correct_ans/")
            else:
                file =  open('temp.cpp')
                file = File(file)
                sol = Solution(
                    user = request.user,
                    problem=problem,
                    language=request.POST['language'],
                    code_file=file,
                    verdict='WA'
                )
                sol.save()
                file.close()
                return HttpResponseRedirect("/submit/wrong_ans/")
        # if user submitted the code using code editor 
        elif codeInEditor:
            # copy the code to temp.cpp
            byte_content = codeInEditor.encode()
            with open('temp.cpp' , 'wb+') as temp_code:
                temp_code.write(byte_content)
            temp_code.close()
            # open some useful files and write desired content
            expout = open('exp_out.txt' , 'w')
            output = open('output.txt' , 'w')
            expout.write(test.test_output)
            # get verdict
            input = bytes(test.test_input , 'utf-8')
            verdict = runcode(input, output)
            expout.close()
            verdict = get_verdict()

            if verdict == 'AC':
                # file =  open('temp.cpp')
                # myfile = File(file)
                # sol = Solution(
                #     user = request.user,
                #     problem=problem,
                #     language=request.POST['language'],
                #     code_file=file,
                #     verdict='AC'
                # )
                # sol.save()
                # file.close()
                return HttpResponseRedirect("/submit/correct_ans/")
            else:
                # file =  open('temp.cpp')
                # myfile = File(file)
                # sol = Solution(
                #     user = request.user,
                #     problem=problem,
                #     language=request.POST['language'],
                #     code_file=file,
                #     verdict='WA'
                # )
                # sol.save()
                # file.close()
                return HttpResponseRedirect("/submit/wrong_ans/")
            # return HttpResponse('Yep! I got your code')
        else:
            return HttpResponse('No code file uploaded!!')
    else:
        return HttpResponse('Usage: Post method is not used.')



def compile_code(code, language):
    if language == "cpp":
        # Compile C++ code using g++
        try:
            process = subprocess.run(["g++", "-o", "program", "-x", "c++", "-"], input=code, capture_output=True, text=True, timeout=10)
            if process.returncode != 0:
                # Compilation error occurred
                error_message = process.stderr.strip()
                return False, error_message
            else:
                # Compilation succeeded
                return True, None
        except subprocess.TimeoutExpired:
            # Compilation timed out
            return False, "Compilation timed out"
    else:
        # Unsupported language
        return False, "Unsupported language"

# Example usage
code = "#include<bits/stdc++.h>\nusing namespace std; int main(){ return 0; }"
success, error_message = compile_code(code, "cpp")
if success:
    print("Compilation succeeded")
else:
    print(f"Compilation failed: {error_message}")
