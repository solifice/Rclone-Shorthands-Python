from colorama import init, Fore, Style

class InputOutputFileOperations:       
    def get_value_from_file(self, file_path, variable_name):

        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if variable_name in line:
                        variable_value = line.split('=')[1].strip()
                        if variable_value == '':
                            return None
                        variable_value = variable_value.strip()
                        return variable_value
        except FileNotFoundError:
            pass
        return None
        
    def get_value_from_user(self, variable_name, prompt, existing_value):

        variable_value = input(prompt)
        if variable_value.strip() == '':
            print(f"{Fore.LIGHTYELLOW_EX}  You didn't provide any value, Skipping.{Style.RESET_ALL}")
            return existing_value
        return variable_value.strip()
        
    def put_value_to_file(self, file_path, variable_name, variable_value):

        if is_value_available(variable_value):
            try:
                with open(file_path, 'r') as f:
                    lines = f.readlines()

                is_variable_present = False
                for i, line in enumerate(lines):
                    if line.startswith(variable_name + '='):
                        variable_value = variable_value.strip()
                        lines[i] = f"{variable_name}={variable_value}\n"
                        is_variable_present = True
                        break
                if not is_variable_present:
                    lines.append(f"{variable_name}={variable_value}\n")

                with open(file_path, 'w') as f:
                    f.writelines(lines)

            except Exception as e:
                print(f"Error writing to file: {e}")

    def is_value_available(self, variable_value):
        
        return variable_value is not None
        
#---------------------------------------------------------------------------------------------------------------------