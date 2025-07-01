import os
import sys
import subprocess
import json
import yaml
import openpyxl
from openpyxl import Workbook, load_workbook
from filecmp import cmp
import shutil
import datetime
from openpyxl.utils import get_column_letter
 
def clone_repo(repo_url, branch_name, target_folder):
    try:
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)
        os.makedirs(target_folder)  # Create the target folder
    except Exception as e:
        print(f"Error creating folder '{target_folder}': {e}")
        return
 
    # Clone the specified branch into the target folder
    try:
        subprocess.run(
            ["git", "clone", "--branch", branch_name, repo_url, target_folder],
            check=True
        )
        print(f"Successfully cloned '{branch_name}' branch into '{target_folder}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning the repository: {e}")
 
def copy_missing_yaml_files(higher_env_x_1, lower_env_x, lower_env, higher_env):
    """
    Compares YAML files in two folders and copies missing files
    from the lower environment to the higher environment.
 
    Args:
        higher_env_x_1 (str): Path to the higher environment folder.
        lower_env_x (str): Path to the lower environment folder.
    """
 
    higher_env_x_1_files = set(os.listdir(higher_env_x_1))
    lower_env_x_files = set(os.listdir(lower_env_x))
 
    # Identify YAML files present in lower_env_x but not in higher_env_x_1
    missing_files = [f for f in lower_env_x_files if f.endswith(('.yaml', '.yml')) and f not in higher_env_x_1_files]
 
    for filename in missing_files:
        source_path = os.path.join(lower_env_x, filename)
        destination_path = os.path.join(higher_env_x_1, filename)
 
        try:
            shutil.copy2(source_path, destination_path)  # copy2 preserves metadata
 
        except Exception as e:
            print(f"Error copying {filename}: {e}")
 
        try:
            with open(destination_path, 'r') as file:
                file_content = file.read()  # Read the entire file into a string [1][2]
 
            # Replace the string
            updated_content = file_content.replace(lower_env, higher_env)  # Replace occurrences of the old string with the new string [2][3][4]
 
            with open(destination_path, 'w') as file:
                file.write(updated_content)  # Write the updated content back to the file [2]
 
            # print(f"Successfully replaced '{lower_env}' with '{higher_env}' in '{filename}'.")
 
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
 
    if not os.path.exists(higher_env_x_1):
        print(f"Error: The folder {higher_env_x_1} does not exist.")
    if not os.path.exists(lower_env_x):
        print(f"Error: The folder {lower_env_x} does not exist.")
 
def create_release_note_summary(files_path, release_note, input_sheet_name):
    """
    Finds YAML files in a specified path, lists service names in an Excel sheet,
    adds a dropdown for status, and populates status based on another sheet.
    """
 
    # Initialize excel_file variable
    excel_file = None
 
    # Check if release_note directory exists and find the Excel file
    if os.path.exists(release_note):
        for i in os.listdir(release_note):
            if i.endswith(".xlsx"):
                excel_file = os.path.join(release_note, i)
                break  # Exit loop once the first Excel file is found
 
    if not excel_file:
        print("Excel sheet not found in the specified directory.")
        return  # Exit the function if no Excel file is found
 
    # Get YAML files from the specified path
    yaml_files = [f for f in os.listdir(files_path) if f.endswith('.yaml') or f.endswith('.yml')]
 
    # Load the existing workbook or create a new one if needed
    wb = openpyxl.load_workbook(excel_file)
 
    # Check if "Summary" sheet already exists; if so, remove it
    if "Summary" in wb.sheetnames:
        del wb["Summary"]
 
    # Create a new "Summary" sheet
    summary_sheet = wb.create_sheet("Summary")
    summary_sheet.sheet_state = "visible"
 
    # Add column headers
    headers = ["Services", "Status", "Comments", "Owner"]
    summary_sheet.append(headers)
 
    # Add service names from YAML files
    for yaml_file in yaml_files:
        service_name = os.path.splitext(yaml_file)[0]  # Use file name (without extension) as service name
        summary_sheet.append([service_name])
 
    # Add dropdown options to the "Status" column
    dropdown_options = ["Updated", "No modifications", "New service", "Deleted service"]
 
    # Data validation for dropdowns
    dv = openpyxl.worksheet.datavalidation.DataValidation(
        type="list",
        formula1='"{}"'.format(",".join(dropdown_options)),
        allow_blank=True
    )
 
    # Add the dropdown to all cells in the "Status" column (from row 2 onwards)
    for row in range(2, summary_sheet.max_row + 1):
        col = 2  # "Status" column
        cell = summary_sheet.cell(row=row, column=col)
        dv.add(cell.coordinate)
 
    summary_sheet.add_data_validation(dv)
 
    # Load the specified sheet for comments
    if input_sheet_name in wb.sheetnames:
        comments_sheet = wb[input_sheet_name]
    else:
        print(f"Sheet '{input_sheet_name}' not found in the Excel file.")
        return
 
    # Iterate through service names in the Summary sheet
    for row in range(2, summary_sheet.max_row + 1):
        service_name = summary_sheet.cell(row=row, column=1).value
 
        # Find matching service in the comments sheet
        for comments_row in range(2, comments_sheet.max_row + 1):
            if comments_sheet.cell(row=comments_row, column=1).value == service_name:
                comment = comments_sheet.cell(row=comments_row, column=comments_sheet.max_column).value  # Assuming comments are in the last column
 
                # Update status based on the comment
                if comment == "root object added":
                    summary_sheet.cell(row=row, column=2).value = "New service"
                elif comment == "root object deleted":
                    summary_sheet.cell(row=row, column=2).value = "Deleted service"
                elif comment in ["Modified", "Added"]:
                    summary_sheet.cell(row=row, column=2).value = "Updated"
                break  # Exit loop if match found
        else:
            # If no match found, set status to "No modifications"
            summary_sheet.cell(row=row, column=2).value = "No modifications"
 
    # Adjust column widths for better readability
    for col in range(1, 5):  # Adjust columns A to D
        column_letter = get_column_letter(col)
        summary_sheet.column_dimensions[column_letter].width = 20
 
    input_sheet_name = ''
    # Save the workbook with the updated Summary sheet
    wb.save(excel_file)
 
 
    wb = openpyxl.load_workbook(excel_file)
 
    if "Summary" in wb.sheetnames:
        sheet = wb["Summary"]  # Corrected from wb.sheetname to wb["Summary"]
 
        # Get the current index of the sheet
        current_index = wb._sheets.index(sheet)
 
        # If the sheet is not already the first one, move it
        if current_index != 0:
            # Remove the sheet from its current position
            wb._sheets.pop(current_index)
            # Insert the sheet at the beginning
            wb._sheets.insert(0, sheet)
 
        wb.save(excel_file)
 
def fetch_json(target_folder, env):
    json_path = ''
    foldername = f"{env}-values"
    for root, folders, files in os.walk(target_folder):
        if foldername in folders:
            lower_env_path = os.path.join(root, foldername, 'app-values')
            for filename in os.listdir(lower_env_path):
                if filename == f"config-{env}.json":
                    json_path = os.path.join(lower_env_path, filename)
                    break
            if not json_path:
                # Create an empty config-dev.json if it doesn't exist
                json_path = os.path.join(lower_env_path, f"config-{env}.json")
                with open(json_path, 'w') as f:
                    json.dump({}, f)  # Create an empty JSON object
            break  # Exit after processing the 'dev-values' folder
 
    return json_path
 
def yaml_to_json(folder_path):
    json_data = {}
    # Convert YAML files to JSON structure
    for filename in os.listdir(folder_path):
        if filename.endswith('.yaml'):
            yaml_path = os.path.join(folder_path, filename)
            with open(yaml_path, 'r') as yaml_file:
                yaml_content = yaml.safe_load(yaml_file)
                json_data[filename[:-5]] = yaml_content  # Use filename without .yaml as the root key
 
    return json_data
 
def compare_json_files(lower_env_x_1, lower_env_x, higher_env_x_1, higher_env_x, envs):
    """
    Compares lower_env x-1 vs x, and collects values for all columns as per new release note format.
    """
    changes = []
    all_services = set(lower_env_x_1.keys()) | set(lower_env_x.keys())
    for service in all_services:
        old = lower_env_x_1.get(service)
        new = lower_env_x.get(service)
        ho = higher_env_x_1.get(service, {})
        hn = higher_env_x.get(service, {})
        if old is None:
            changes.append([service, 'add', '',json.dumps(new, indent=2), '', '', '', 'root object added'
            ])
        elif new is None:
            changes.append([
                service, 'delete', '',
                '', json.dumps(old, indent=2), '', json.dumps(ho, indent=2), 'root object deleted'
            ])
        else:
            compare(
                old, new, ho, hn, service, '', changes, envs
            )
    return changes
 
def compare(old, new, higher_old, higher_new, service, path, changes, envs):
    if isinstance(old, dict) and isinstance(new, dict):
        all_keys = set(old.keys()) | set(new.keys())
        for k in all_keys:
            new_path = f"{path}//{k}" if path else k
            o = old.get(k)
            n = new.get(k)
            ho = higher_old.get(k) if isinstance(higher_old, dict) else None
            hn = higher_new.get(k) if isinstance(higher_new, dict) else None
            if o is not None and n is not None:
                compare(o, n, ho, hn, service, new_path, changes, envs)
            elif o is None:
                changes.append([
                    service, 'add', new_path,
                    json.dumps(n, indent=2), '', '', '', 'Added'
                ])
            elif n is None:
                changes.append([
                    service, 'delete', new_path,
                    '', json.dumps(o, indent=2), '', '', 'Deleted'
                ])
    elif isinstance(old, list) and isinstance(new, list):
        if all(isinstance(i, dict) and "name" in i for i in old+new if i):
            compare_list_of_dicts(
                old, new,
                higher_old if isinstance(higher_old, list) else [],
                higher_new if isinstance(higher_new, list) else [],
                service, path, changes, envs
            )
        else:
            max_len = max(len(old), len(new))
            for i in range(max_len):
                o = old[i] if i < len(old) else None
                n = new[i] if i < len(new) else None
                ho = higher_old[i] if isinstance(higher_old, list) and i < len(higher_old) else None
                hn = higher_new[i] if isinstance(higher_new, list) and i < len(higher_new) else None
                idx_path = f"{path}//[{i}]"
                if o is not None and n is not None:
                    compare(o, n, ho, hn, service, idx_path, changes, envs)
                elif o is None:
                    changes.append([
                        service, 'add', idx_path,
                        json.dumps(n, indent=2), '', '', '', 'Added'
                    ])
                elif n is None:
                    changes.append([
                        service, 'delete', idx_path,
                        '', json.dumps(o, indent=2), '', '', 'Deleted'
                    ])
    else:
        if old != new:
            # As per your request, higher env values are always empty for now
            changes.append([
                service, 'modify', path,
                json.dumps(new, indent=2), json.dumps(old, indent=2), '', '', 'Modified'
            ])
 
def compare_list_of_dicts(old_list, new_list, higher_old_list, higher_new_list, service, path, changes, envs):
    old_dict = {item["name"]: item for item in old_list if isinstance(item, dict) and "name" in item}
    new_dict = {item["name"]: item for item in new_list if isinstance(item, dict) and "name" in item}
    ho_dict = {item["name"]: item for item in higher_old_list if isinstance(item, dict) and "name" in item}
    hn_dict = {item["name"]: item for item in higher_new_list if isinstance(item, dict) and "name" in item}
    all_names = set(old_dict.keys()) | set(new_dict.keys())
    for name in all_names:
        o = old_dict.get(name)
        n = new_dict.get(name)
        ho = ho_dict.get(name)
        hn = hn_dict.get(name)
        name_path = f"{path}//name={name}" if path else f"name={name}"
        if o is not None and n is not None:
            compare(o, n, ho, hn, service, name_path, changes, envs)
        elif o is None:
            changes.append([
                service, 'add', name_path,
                json.dumps(n, indent=2), '', '', '', 'Added'
            ])
        elif n is None:
            changes.append([
                service, 'delete', name_path,
                '', json.dumps(o, indent=2), '', '', 'Deleted'
            ])
 
def write_changes_to_excel(changes, release_note_path, envs, env_list=None):
    if not changes:
        print("No differences found; skipping the creation of release note.")
        return
 
    # Constant part of the filename
    base_filename = "release-note"
    # Get the current date and time
    now = datetime.datetime.now()
    # Format the date and time as a string
    date_time_str = now.strftime("%d-%b-%Y-%H-%M-%S")
    # Create the complete filename
    excel_file = f"{base_filename}-{date_time_str}.xlsx"
    excel_file_path = os.path.join(release_note_path, excel_file)
 
    # Always create a new workbook for the release note
    wb = Workbook()
    ws = wb.active
    ws.title = envs[1]  # Sheet name as higher env
 
    # New columns as per requirement
    columns = [
        'Service name', 'Change Request', 'Key',
        f'{envs[0]}-current value', f'{envs[0]}-previous value',
        f'{envs[1]}-current value', f'{envs[1]}-previous value',
        'Comment'
    ]
    ws.append(columns)
 
    for change in changes:
        # change: [service, change_type, key, l_cur, l_prev, h_cur, h_prev, comment]
        # h_cur and h_prev are always empty per your instruction
 
        service, change_type, key, l_cur, l_prev, h_cur, h_prev, comment = change
 
        # Check if value exceeds 32,767 characters
        if len(l_cur) > 32767:
            # Save large data to a text file
            txt_file_name = f"{service}.txt"
            txt_file_path = os.path.join(release_note_path, txt_file_name)
            with open(txt_file_path, 'w') as txt_file:
                txt_file.write(l_cur)
 
            # Format path for hyperlink (absolute path)
            txt_file_path_linked = f'file:///{os.path.abspath(txt_file_path)}'.replace(' ', '%20')
 
            # Create a hyperlink in Excel pointing to this text file
            ws.append([service,change_type,key,f'=HYPERLINK("{txt_file_path_linked}")',l_prev, h_cur, h_prev, comment])
        else:
            # Append new changes directly to the relevant sheet
            row = [
            change[0], change[1], change[2],
            change[3], change[4], '', change[6], change[7]
        ]
        ws.append(row)
 
 
 
 
 
 
 
 
 
    wb.save(excel_file_path)
    print(f"Release note written to {excel_file_path}")
 
 
def get_input(prompt):
    attempts = 3
    for _ in range(attempts):
        value = input(prompt)
        if value:
            return value
        print("Input cannot be empty. Please try again.")
    print("Cannot proceed with execution as no input was entered.")
    exit(1)
 
def compare_shell_scripts(folder_x_1, folder_x, release_note_path, env):
    # Define paths to the scripts folders in each branch
    scripts_folder_x_1 = os.path.join(folder_x_1, f'helm-charts/{env}-values/db-scripts')
    scripts_folder_x = os.path.join(folder_x, f'helm-charts/{env}-values/db-scripts')
 
    # Check if the scripts folders exist
    if not os.path.isdir(scripts_folder_x_1) or not os.path.isdir(scripts_folder_x):
        print("Scripts folder not found in one or both branches.")
        return
 
    # List of modified shell scripts for each subfolder
    modified_scripts_x_1 = {}
    modified_scripts_x = {}
 
    # Iterate through subfolders in scripts_folder_x_1
    for subfolder in os.listdir(scripts_folder_x_1):
        subfolder_path_x_1 = os.path.join(scripts_folder_x_1, subfolder)
        if os.path.isdir(subfolder_path_x_1):
            modified_scripts_x_1[subfolder] = []
            modified_scripts_x[subfolder] = []
 
            # Check if the subfolder exists in scripts_folder_x
            subfolder_path_x = os.path.join(scripts_folder_x, subfolder)
            if os.path.isdir(subfolder_path_x):
                # Compare files in both subfolders
                for filename in os.listdir(subfolder_path_x):
                    if (filename.endswith('.sh') or filename.endswith('.sql') or filename.endswith('.aql')) and filename in os.listdir(subfolder_path_x_1):
                        file_path_x_1 = os.path.join(subfolder_path_x_1, filename)
                        file_path_x = os.path.join(subfolder_path_x, filename)
                        if not cmp(file_path_x_1, file_path_x, shallow=False):
                            modified_scripts_x_1[subfolder].append(filename)
                            modified_scripts_x[subfolder].append(filename)
            else:
                print(f"Subfolder {subfolder} not found in {scripts_folder_x}.")
 
    # If there are modified scripts, add a new sheet in the workbook
    if any(modified_scripts_x_1.values()):
        print("The modified sql scripts are: ")
        for subfolder, scripts in modified_scripts_x_1.items():
            print(f"{subfolder}: {scripts}")
 
        if os.path.exists(release_note_path):
            for i in os.listdir(release_note_path):
                if i.endswith(".xlsx"):
                    excel_file = os.path.join(release_note_path, i)
                    excel_file_path = os.path.join(release_note_path, excel_file)
 
                    if not os.path.exists(excel_file_path):
                        wb = Workbook()
                    else:
                        wb = load_workbook(excel_file_path)
 
                    if "DB-scripts-summary" in wb.sheetnames:
                        ws = wb["DB-scripts-summary"]
                    else:
                        ws = wb.create_sheet(title="DB-scripts-summary")
 
                    # Add subfolder names as column headers
                    headers = [f'{subfolder} (Folder {scripts_folder_x_1.split("/")[-2]})' for subfolder in modified_scripts_x.keys()]
                    ws.append(headers)
 
                    # Write the list of modified scripts
                    max_scripts = max(len(scripts) for scripts in modified_scripts_x.values())
                    for i in range(max_scripts):
                        row = []
 
                        for subfolder in modified_scripts_x.keys():
                            if i < len(modified_scripts_x[subfolder]):
                                row.append(modified_scripts_x[subfolder][i])
                            else:
                                row.append("")
                        ws.append(row)
 
                    # Save the updated workbook
                    wb.save(excel_file_path)
        else:
            print("Release note path does not exist.")
 
    else:
        print(f"No modified scripts found in {scripts_folder_x_1}.")
 
 
def execute(target_folder_x, lower_env, higher_env, repo_url):
    try:
        release_note_path = os.path.join(target_folder_x, "release_note")
        if os.path.exists(release_note_path) and os.path.isdir(release_note_path):
            print(f"Checking folder: {release_note_path}")
 
            # List all files in the directory
            for filename in os.listdir(release_note_path):
                # Check if the file ends with .xlsx
                if filename.endswith('.xlsx'):
                    file_path = os.path.join(release_note_path, filename)
                    print("This is the file path for db-scripts: ",file_path)
                    result = subprocess.run(
                        ["python3.11", sys.argv[6] ,repo_url, lower_env,higher_env, file_path],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    return result.stdout
                else:
                    print("Excel file not found")
 
 
    except subprocess.CalledProcessError as e:
        print("Script failed to execute.")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
 
 
def create_upgrade_services_txt(excel_path, sheet_name, repo_root, envs):
    # Path to the output file in the root of the repo
    txt_path = os.path.join(repo_root, 'upgrade-services.txt')
 
    # Delete the file if it already exists
    if os.path.exists(txt_path):
        os.remove(txt_path)
 
    excel_folder = os.listdir(excel_path)
    for i in excel_folder:
        if i.endswith(".xlsx"):
            file_path = os.path.join(excel_path,i)
 
    wb = load_workbook(file_path)
    ws = wb[sheet_name]
 
    # Find column indices by header names
    headers = [cell.value for cell in ws[1]]
    try:
        key_col = headers.index('Key') + 1
        service_name_col = headers.index('Service name') + 1
        value_col = headers.index(f'{envs[0]}-current value') + 1
    except ValueError as e:
        raise ValueError(f"Required column missing: {e}")
 
    with open(txt_path, 'w') as file:
        for row in ws.iter_rows(min_row=2):
            key_cell = row[key_col - 1].value
            if (key_cell and 'image//tag' in str(key_cell)) or (key_cell and 'image//image_name' in str(key_cell)):
                print(key_cell)
                service_name = row[service_name_col - 1].value
                value = row[value_col - 1].value
                if service_name is not None and value is not None:
                    file.write(f"{service_name}:{value}\n")
                    print(f"fileeenameee:: {service_name}:{value}\n")
 
def main():
    repos_info = {
        'promo-helm-charts': sys.argv[5]
    }
 
    for repo_name, repo_url in repos_info.items():
        # promote_branch_x_1 = input("Enter the branch containing the stable release: ")
        promote_branch_x_1 = sys.argv[1]
        # promote_branch_x = input("Enter the branch containing the updated files for release: ")
        promote_branch_x = sys.argv[2]
        target_folder_x_1 = os.path.join(os.getcwd(), "generate-config", "promotion-x-1", f"{repo_name}")
        target_folder_x = os.path.join(os.getcwd(), "generate-config", "promotion-x", f"{repo_name}")
    envs = []
    envs.append(sys.argv[3].strip())
    envs.append(sys.argv[4].strip())
    print("The list of envs is",envs)
    env_list = ['dev2', 'sit2', 'uat2', 'prod']
    # Environment list (you can modify based on your use case)
    # envs = ['dev', 'sit', 'uat', 'preprod', 'perf', 'mig/dm', 'sec', 'prod']
 
    # To Clone the repo from promotion-x-1 branch
    clone_repo(repo_url, promote_branch_x_1, target_folder_x_1)
 
    # To Clone the repo from promotion-x branch
 
    clone_repo(repo_url, promote_branch_x, target_folder_x)
 
    if envs[0].startswith('dev'):
        print("dev2 is the lower-env")
        #to create the release note folder
        release_note_path = os.path.join(target_folder_x, "helm-charts", f"{envs[1]}-values", f"release_note")
        if os.path.exists(release_note_path) and os.path.isdir(release_note_path):
            print(f"Checking folder: {release_note_path}")
 
            # List all files in the directory
            for filename in os.listdir(release_note_path):
                # Check if the file ends with .xlsx
                if filename.endswith('.xlsx'):
                    file_path = os.path.join(release_note_path, filename)
                    try:
                        os.remove(file_path)  # Delete the file
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")
        else:
            print(f"Folder does not exist: {release_note_path}, hence creating one")
        if not os.path.exists(release_note_path):
            os.makedirs(release_note_path)
 
        higher_env_x_1 = os.path.join(target_folder_x_1, f"helm-charts/{envs[1]}-values/app-values")
        lower_env_x = os.path.join(target_folder_x, f"helm-charts/{envs[0]}-values/app-values")
 
        if os.path.exists(higher_env_x_1) and os.path.exists(lower_env_x):
            copy_missing_yaml_files(higher_env_x_1, lower_env_x, envs[0], envs[1])
 
        #To fetch the path of config-dev.json from promotion-x-1 branch
        previous_json_path = fetch_json(target_folder_x_1, envs[0])
        print(previous_json_path)
 
        #To fetch the path of config-dev.json from promotion-x branch
        new_json_path = fetch_json(target_folder_x, envs[0])
        print(new_json_path)
 
        # Load previous JSON data
        try:
            with open(previous_json_path, 'r') as old_file:
                old_data = json.load(old_file)
        except (json.JSONDecodeError, FileNotFoundError):
            print("Previous JSON file is invalid or not found.")
            old_data = {}
 
        lower_env_path_x_1 = os.path.dirname(previous_json_path)
        old_data = yaml_to_json(lower_env_path_x_1)
 
        # Save the previous JSON data
        with open(previous_json_path, 'w') as previous_json_file:
            json.dump(old_data, previous_json_file, indent=4)
 
        lower_env_path_x = os.path.dirname(new_json_path)
        json_data = yaml_to_json(lower_env_path_x)
 
        # Save the new JSON data
        with open(new_json_path, 'w') as new_json_file:
            json.dump(json_data, new_json_file, indent=4)
 
        # --- NEW: Load higher env data for both x-1 and x ---
        higher_env_x_1_path = os.path.join(target_folder_x_1, f"helm-charts/{envs[1]}-values/app-values")
        higher_env_x_path = os.path.join(target_folder_x, f"helm-charts/{envs[1]}-values/app-values")
        higher_env_x_1 = yaml_to_json(higher_env_x_1_path)
        higher_env_x = yaml_to_json(higher_env_x_path)
 
        # --- UPDATED: Compare JSON files with all required arguments ---
        changes = compare_json_files(
            old_data,           # lower_env_x_1
            json_data,          # lower_env_x
            higher_env_x_1,     # higher_env_x_1
            higher_env_x,       # higher_env_x
            envs                # envs
        )
 
        # Write changes to Excel with multiple sheets
        write_changes_to_excel(changes, release_note_path, envs, env_list)
 
        result = execute(target_folder_x, envs[0], envs[1], repo_url)
        print(result)
 
        create_upgrade_services_txt(release_note_path, envs[1], target_folder_x, envs)
 
    else:
        print("dev2 is not the lower-env")
        release_note_path = os.path.join(target_folder_x, "helm-charts", f"{envs[1]}-values", f"release_note")
        if os.path.exists(release_note_path) and os.path.isdir(release_note_path):
            print(f"Checking folder: {release_note_path}")
 
            # List all files in the directory
            for filename in os.listdir(release_note_path):
                # Check if the file ends with .xlsx
                if filename.endswith('.xlsx'):
                    excel_file = os.path.join(release_note_path, filename)
                    break
 
 
        if not excel_file:
            print(f"No Excel release note file found in {release_note_path}.")
            return
 
        wb = openpyxl.load_workbook(excel_file)
        if envs[0] not in wb.sheetnames:
            print(f"Sheet '{envs[0]}' not found in the Excel file.")
            return
 
        sheet = wb[envs[0]]
 
        # Check column D (4th column) for any filled cells from row 2 onwards
        values_present = False
        for row in sheet.iter_rows(min_row=2, min_col=4, max_col=4):
            cell = row[0]
            if cell.value not in (None, '', ' '):
                values_present = True
            else:
                print("771")
 
        if values_present:
            print(f"Values are already available in column D of sheet '{envs[0]}'. No release note creation required.")
        else:
            # Optionally handle the case where column D is empty
            print(f"No values found in column D of sheet '{envs[0]}'. Proceeding as needed.")
            # You can decide to run the usual process or handle differently
        result = execute()
        print(result)
 
        create_upgrade_services_txt(release_note_path, envs[1], target_folder_x, envs)
 
    root_folders = os.listdir(target_folder_x)
 
    print(f"Contents of folder '{target_folder_x}':")
    for folder in root_folders:
        if folder == "release_note":
            release_note_folder = os.path.join(target_folder_x,folder)
            for i in folder:
                if i.endswith('xlsx'):
                    release_note = os.path.join(release_note_folder,i)
                    print("file exists: ", release_note)
 
    try:
        subprocess.run(['git', 'add', "."], cwd =target_folder_x, check=True, capture_output=True, text=True)
        status_result = subprocess.run(['git', 'status'], cwd =target_folder_x, check=True, capture_output=True, text=True)
        print(status_result.stdout)
        print(status_result.stderr)
        # Pull latest changes with rebase to avoid non-fast-forward errors
        subprocess.run(['git', 'config', 'user.email', 'surabhi.h@qwerty.com'], cwd =target_folder_x ,check=True, timeout=30)
        subprocess.run(['git', 'config', 'user.name', ''], cwd =target_folder_x, check=True, timeout=30)
        subprocess.run(['git', 'commit', '-m',
                    f'Pushing the release_note into the branch: {sys.argv[2]} '], cwd =target_folder_x, check=True, capture_output=True, text=True)
        subprocess.run(['git', 'pull', '--rebase', 'origin', sys.argv[2]], cwd=target_folder_x, check=True, capture_output=True, text=True)
        print("Pulled latest changes successfully.")
 
        # Push changes
        push_result = subprocess.run(['git', 'push', 'origin', sys.argv[2]], cwd=target_folder_x, check=True, capture_output=True, text=True)
        print("Push successful:")
        print(push_result.stdout)
 
    except subprocess.CalledProcessError as e:
        print("Git command failed!")
        print("Return code:", e.returncode)
        print("Command:", e.cmd)
        print("Output:", e.output)
        print("Error:", e.stderr)
        sys.exit(1)
 
    target_folder_x = os.path.dirname(target_folder_x)
    target_folder_x_1 = os.path.dirname(target_folder_x_1)
 
if __name__ == '__main__':
    main()
 
 