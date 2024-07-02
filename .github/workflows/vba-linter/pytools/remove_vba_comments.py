import sys
import os

def run(input_file_path, output_file_path):
    try:
        # Ensure the destination directory exists
        destination_dir = os.path.dirname(output_file_path)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # Open the input and output files in binary mode
        with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:

            # Initialize a flag to indicate whether a double-quote string is in progress
            quote_in_progress = False
            
            # Initialize a flag to indicate whether a comment is in progress
            comment_in_progress = False

            # Initialize a flag to indicate whether a line break is in progres (inside a comment)
            linebreak_in_progress = False

            multi_line_comment = False

            # Initialize a variable to store the modified line
            modified_content = bytearray()

            # Store the on-going comment
            ongoing_comment = bytearray()

            # Iterate through the bytes in the input file
            for byte in input_file.read():
                # If a double-quote string is in progress, add bytes to the modified line
                if quote_in_progress:
                    modified_content.append(byte)
                    # Check if the current byte corresponds to the end of the double-quote string
                    if byte == 34:  # ASCII code for double-quote
                        quote_in_progress = False
                # If a single quote is encountered outside a string, start a comment
                elif comment_in_progress:
                    
                    if linebreak_in_progress:
                        if byte != 10: # ASCII code for \n (LF)
                            print(f"Expected file {input_file_path} to have CRLF line endings.")
                            sys.exit(1) 
                        linebreak_in_progress = False

                        if not multi_line_comment:
                            comment_in_progress = False
                            multi_line_comment = False
                        
                        modified_content.extend(b'\r\n')  # Append bytes for line break (CRLF)

                    else:
                        if byte == 13: # ASCII code for \r (CR)
                            linebreak_in_progress = True
                            if ongoing_comment[-1:] == b'_':
                                multi_line_comment = True
                        else:
                            ongoing_comment.append(byte)
                        
                elif byte == 39:  # ASCII code for single-quote
                    # reset the comment array
                    ongoing_comment = bytearray()
                    ongoing_comment.append(byte)
                    comment_in_progress = True

                # If it's not a comment or string character, add it to the modified line
                else:
                    modified_content.append(byte)

            # Write the modified line to the output file
            output_file.write(modified_content)

        print(f"VBA comments removed. Filtered content saved to {output_file_path}")
        return "Success"
    except FileNotFoundError:
        return f"Error: remove_vba_comments - file not found: {input_file_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

