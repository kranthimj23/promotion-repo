"""
Git helper functions for Test Data Generator CRN

This module provides reusable git operations to eliminate code duplication
across promotion, release note generation, and configuration management scripts.

Functions:
- is_base_branch_exists: Check if a branch exists in remote repository
- clone_single_branch_and_checkout: Clone a single branch from repository
- clone_branch_and_checkout_new_branch: Clone base branch and create new branch
- clone_repo_and_checkout: Clone repository and checkout specific branch
- stage_commit_and_push: Stage changes, commit with message, and push to branch

"""

import subprocess
import os
import shutil
import tempfile
from pathlib import Path


def run_git_command(cmd, cwd=None, shell=True, timeout=30):
    """
    Execute a git command and return output.

    Args:
        cmd (str or list): Git command to execute
        cwd (str): Working directory for command execution
        shell (bool): Whether to use shell=True
        timeout (int): Command timeout in seconds

    Returns:
        str: Command output (stdout)

    Raises:
        subprocess.CalledProcessError: If command fails
    """
    print(f"Running: {cmd} in {cwd or os.getcwd()}")

    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed!")
        print(f"Return Code: {e.returncode}")
        print(f"Command: {e.cmd}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise


def inject_git_token(repo_url, github_token=None):
    """
    Inject GitHub token into repository URL for authentication.

    Args:
        repo_url (str): Repository URL (HTTPS format)
        github_token (str): GitHub personal access token (optional)

    Returns:
        str: Repository URL with token injected (if provided)

    Raises:
        ValueError: If URL is not HTTPS format
    """
    import os

    if not github_token:
        github_token = os.getenv("GIT_TOKEN")

    if github_token and "github.com" in repo_url:
        if repo_url.startswith("https://"):
            return repo_url.replace("https://", f"https://{github_token}@")
        else:
            raise ValueError("Unsupported repo_url format. Must start with https://")

    return repo_url


def is_base_branch_exists(repo_url, branch_name):
    """
    Check if a branch exists in the remote repository.

    Args:
        repo_url (str): Repository URL
        branch_name (str): Branch name to check

    Returns:
        bool: True if branch exists, False otherwise
    """
    try:
        result = subprocess.run(
            ['git', 'ls-remote', '--heads', repo_url, branch_name],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error checking branch existence: {e.stderr}")
        return False


def clone_single_branch_and_checkout(repo_url, branch_name, target_folder, depth=None):
    """
    Clone a single branch from repository and checkout.

    Args:
        repo_url (str): Repository URL
        branch_name (str): Branch to clone
        target_folder (str): Destination folder
        depth (int): Clone depth (optional, for shallow clone)

    Returns:
        str: Path to cloned repository

    Raises:
        RuntimeError: If clone fails
    """
    # Clean and create target folder
    try:
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)
        os.makedirs(target_folder)
    except Exception as e:
        print(f"Error creating folder '{target_folder}': {e}")
        raise

    # Build clone command
    cmd = ['git', 'clone', '--branch', branch_name, '--single-branch']

    if depth:
        cmd.extend(['--depth', str(depth)])

    cmd.extend([repo_url, target_folder])

    try:
        print(f"Cloning branch '{branch_name}' from {repo_url}")
        subprocess.run(cmd, check=True, timeout=30, stdout=subprocess.DEVNULL)
        print(f"Successfully cloned '{branch_name}' branch into '{target_folder}'.")
        return target_folder
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        raise RuntimeError(f"Git clone failed: {e.stderr}")


def clone_branch_and_checkout_new_branch(repo_url, base_branch, new_branch, target_folder):
    """
    Clone repository from base branch and create a new branch from it.

    Args:
        repo_url (str): Repository URL
        base_branch (str): Base branch to clone from
        new_branch (str): New branch name to create
        target_folder (str): Destination folder

    Returns:
        str: Path to repository with new branch checked out

    Raises:
        RuntimeError: If clone or branch creation fails
    """
    # Clean and create target folder
    try:
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)
        os.makedirs(target_folder)
    except Exception as e:
        print(f"Error creating folder '{target_folder}': {e}")
        raise

    try:
        # Clone base branch
        print(f"Cloning base branch '{base_branch}' from {repo_url}")
        subprocess.run(
            ['git', 'clone', '--single-branch', '-b', base_branch, repo_url, target_folder],
            check=True,
            timeout=30,
            stdout=subprocess.DEVNULL
        )
        print(f"Successfully cloned '{base_branch}' branch.")

        # Create new branch
        print(f"Creating new branch '{new_branch}'")
        subprocess.run(
            ['git', 'checkout', '-b', new_branch],
            cwd=target_folder,
            check=True,
            timeout=30
        )
        print(f"Successfully created and checked out branch '{new_branch}'.")

        return target_folder
    except subprocess.CalledProcessError as e:
        print(f"Error during clone and checkout: {e}")
        raise RuntimeError(f"Clone and checkout failed: {e.stderr}")


def clone_repo_and_checkout(repo_url, branch_name, target_folder):
    """
    Clone repository and checkout specified branch.

    Args:
        repo_url (str): Repository URL
        branch_name (str): Branch to checkout
        target_folder (str): Destination folder

    Returns:
        str: Path to cloned and checked out repository

    Raises:
        RuntimeError: If clone fails
    """
    # Clean and create target folder
    try:
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)
        os.makedirs(target_folder)
    except Exception as e:
        print(f"Error creating folder '{target_folder}': {e}")
        raise

    try:
        print(f"Cloning repository from {repo_url}")
        subprocess.run(
            ['git', 'clone', repo_url, target_folder],
            check=True,
            timeout=30,
            stdout=subprocess.DEVNULL
        )

        # Checkout specific branch
        print(f"Checking out branch '{branch_name}'")
        subprocess.run(
            ['git', 'checkout', branch_name],
            cwd=target_folder,
            check=True,
            timeout=30
        )
        print(f"Successfully cloned and checked out '{branch_name}'.")

        return target_folder
    except subprocess.CalledProcessError as e:
        print(f"Error cloning and checking out: {e}")
        raise RuntimeError(f"Clone and checkout failed: {e.stderr}")


def configure_git_user(repo_path, email="kranthimj23@gmail.com", name="kranthimj23"):
    """
    Configure git user.email and user.name for repository.

    Args:
        repo_path (str): Path to git repository
        email (str): Git user email
        name (str): Git user name

    Raises:
        RuntimeError: If configuration fails
    """
    try:
        subprocess.run(
            ['git', 'config', 'user.email', email],
            cwd=repo_path,
            check=True,
            timeout=30
        )
        subprocess.run(
            ['git', 'config', 'user.name', name],
            cwd=repo_path,
            check=True,
            timeout=30
        )
        print(f"Git user configured: {name} <{email}>")
    except subprocess.CalledProcessError as e:
        print(f"Error configuring git user: {e}")
        raise RuntimeError(f"Git configuration failed: {e.stderr}")


def stage_commit_and_push(
    repo_path,
    branch_name,
    commit_message,
    files_to_stage=".",
    pull_before_push=True,
    use_rebase=True
):
    """
    Stage changes, commit with message, and push to branch.

    Args:
        repo_path (str): Path to git repository
        branch_name (str): Branch to push to
        commit_message (str): Commit message
        files_to_stage (str): Files to stage (default: "." for all)
        pull_before_push (bool): Pull before push (default: True)
        use_rebase (bool): Use rebase when pulling (default: True)

    Raises:
        RuntimeError: If any git operation fails
    """
    try:
        # Stage changes
        print(f"Staging changes: {files_to_stage}")
        subprocess.run(
            ['git', 'add', files_to_stage],
            cwd=repo_path,
            check=True,
            timeout=30,
            capture_output=True
        )

        # Show git status
        print("Git status:")
        status_result = subprocess.run(
            ['git', 'status'],
            cwd=repo_path,
            check=True,
            timeout=30,
            capture_output=True,
            text=True
        )
        print(status_result.stdout)

        # Commit changes
        print(f"Committing with message: {commit_message}")
        subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=repo_path,
            check=True,
            timeout=30,
            capture_output=True
        )
        print("Commit successful.")

        # Pull before push (optional)
        if pull_before_push:
            print(f"Pulling latest changes from origin/{branch_name}")
            pull_cmd = ['git', 'pull']
            if use_rebase:
                pull_cmd.append('--rebase')
            pull_cmd.extend(['origin', branch_name])

            subprocess.run(
                pull_cmd,
                cwd=repo_path,
                check=True,
                timeout=30,
                capture_output=True
            )
            print("Pulled latest changes successfully.")

        # Push changes
        print(f"Pushing to origin/{branch_name}")
        push_result = subprocess.run(
            ['git', 'push', 'origin', branch_name],
            cwd=repo_path,
            check=True,
            timeout=30,
            capture_output=True,
            text=True
        )
        print("Push successful:")
        print(push_result.stdout)

    except subprocess.CalledProcessError as e:
        print("Git command failed!")
        print(f"Return code: {e.returncode}")
        print(f"Command: {e.cmd}")
        print(f"Output: {e.output if hasattr(e, 'output') else 'N/A'}")
        print(f"Error: {e.stderr if hasattr(e, 'stderr') else 'N/A'}")
        raise RuntimeError(f"Git operation failed: {e}")


def stage_specific_files_commit_and_push(
    repo_path,
    branch_name,
    commit_message,
    files_list,
    pull_before_push=True,
    use_rebase=True
):
    """
    Stage specific files, commit with message, and push to branch.

    Args:
        repo_path (str): Path to git repository
        branch_name (str): Branch to push to
        commit_message (str): Commit message
        files_list (list): List of files to stage
        pull_before_push (bool): Pull before push (default: True)
        use_rebase (bool): Use rebase when pulling (default: True)

    Raises:
        RuntimeError: If any git operation fails
    """
    try:
        # Stage specific files
        for file in files_list:
            print(f"Staging file: {file}")
            subprocess.run(
                ['git', 'add', file],
                cwd=repo_path,
                check=True,
                timeout=30,
                capture_output=True
            )

        # Show git status
        print("Git status:")
        status_result = subprocess.run(
            ['git', 'status'],
            cwd=repo_path,
            check=True,
            timeout=30,
            capture_output=True,
            text=True
        )
        print(status_result.stdout)

        # Commit changes
        print(f"Committing with message: {commit_message}")
        subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=repo_path,
            check=True,
            timeout=30,
            capture_output=True
        )
        print("Commit successful.")

        # Pull before push (optional)
        if pull_before_push:
            print(f"Pulling latest changes from origin/{branch_name}")
            pull_cmd = ['git', 'pull']
            if use_rebase:
                pull_cmd.append('--rebase')
            pull_cmd.extend(['origin', branch_name])

            subprocess.run(
                pull_cmd,
                cwd=repo_path,
                check=True,
                timeout=30,
                capture_output=True
            )
            print("Pulled latest changes successfully.")

        # Push changes
        print(f"Pushing to origin/{branch_name}")
        push_result = subprocess.run(
            ['git', 'push', 'origin', branch_name],
            cwd=repo_path,
            check=True,
            timeout=30,
            capture_output=True,
            text=True
        )
        print("Push successful:")
        print(push_result.stdout)

    except subprocess.CalledProcessError as e:
        print("Git command failed!")
        print(f"Return code: {e.returncode}")
        print(f"Command: {e.cmd}")
        print(f"Output: {e.output if hasattr(e, 'output') else 'N/A'}")
        print(f"Error: {e.stderr if hasattr(e, 'stderr') else 'N/A'}")
        raise RuntimeError(f"Git operation failed: {e}")

