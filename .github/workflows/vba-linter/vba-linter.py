import os
import sys
import subprocess
sys.path.insert(0, './.github/workflows/vba-linter/pytools')
import utils
import remove_vba_comments

def needs_conversion_to_crlf(filepath):

    # Use the file command to get information about the file
    file_info = subprocess.check_output(['file', filepath], universal_newlines=True)
    return "with CRLF line terminators" not in file_info


def convert_lf_to_crlf(filepath):
    try:
        # Use the subprocess module to run the unix2dos command
        subprocess.run(["unix2dos", filepath], check=True)
        print(f"✅ Line conversion successful: {filepath}")
    except subprocess.CalledProcessError as e:
        print(f"Error while converting {filepath}: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: unix2dos command not found. Make sure it's installed and in your PATH.")
        sys.exit(1) 


def copy_file(source, destination):
    try:
        # Ensure the destination directory exists
        destination_dir = os.path.dirname(destination)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Open the source file for reading
        with open(source, 'rb') as source_file:
            # Create the destination file and write the contents of the source file to it
            with open(destination, 'wb') as destination_file:
                destination_file.write(source_file.read())
        print(f"File '{source}' copied to '{destination}' successfully.")
    except Exception as e:
        print(f"An error occurred while copying the file: {e}")

# This function assumes that the file is either using LF or CRLF
def is_ascii(filepath):
    try:
        with open(filepath, 'rb') as file:
            char_counter = 0
            line_counter = 1
            for byte in file.read():
                if byte == 10:
                    line_counter = line_counter + 1
                    char_counter = 0
                    continue 
                char_counter = char_counter + 1
                if byte > 127:
                    return f"Problematic byte:'{byte}' at line # '{line_counter}', character #'{char_counter}'"
        return "Success"
    except FileNotFoundError:
        return f"Error: file '{filepath}' not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    package_dir = "/home/runner/work/"  # Replace with the actual path to your package subfolder

    files = []  # Initialize an empty list to store found files

    for root, _, filenames in os.walk(package_dir):
        for filename in filenames:
            if filename.endswith((".bas", ".frm", ".cls")):
                filepath = os.path.join(root, filename)
                files.append(filepath)  # Add found files to the list

                eol_result = needs_conversion_to_crlf(filepath)

                if eol_result:
                    #print(f"⚠ {filepath} doesn't have proper line endings.")
                    convert_lf_to_crlf(filepath)
                    print(f"{filepath} line endings were replaced.")
                else:
                    print(f"{filepath} has correct line endings.")

                destination_no_comments = utils.replace_last_instance(filepath,".","_no_comments.")
                comment_removal_results = remove_vba_comments.run(filepath, destination_no_comments)

                if comment_removal_results != "Success":
                    print(f"comment_removal_results: {comment_removal_results}")
                    sys.exit(1) 

                ascii_result = is_ascii(destination_no_comments)

                if ascii_result == "Success":
                    print(f"{filepath} has correct encoding.")
                else:
                    print(f"ascii_result: {ascii_result}")
                    sys.exit(1)

                os.remove(destination_no_comments)

                print('================================================')

    if not files:
        print("No files with the specified extensions found in the directory.")
    else:
        print(f"Found {len(files)} file(s) with the specified extensions.")

if __name__ == "__main__":
    main()
