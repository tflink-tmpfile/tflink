#!/usr/bin/env python3
"""
Automatic version bumping script for tflink

Usage:
    python bump_version.py patch   # 0.1.0 -> 0.1.1
    python bump_version.py minor   # 0.1.0 -> 0.2.0
    python bump_version.py major   # 0.1.0 -> 1.0.0
    python bump_version.py 0.2.0   # Set to specific version
"""

import re
import sys
import subprocess
from pathlib import Path


def get_current_version():
    """Read current version from __init__.py"""
    init_file = Path("tflink/__init__.py")
    content = init_file.read_text()
    match = re.search(r"__version__ = ['\"]([^'\"]+)['\"]", content)
    if not match:
        print("❌ Error: Could not find __version__ in tflink/__init__.py")
        sys.exit(1)
    return match.group(1)


def parse_version(version_str):
    """Parse version string into (major, minor, patch)"""
    parts = version_str.split('.')
    if len(parts) != 3:
        print(f"❌ Error: Invalid version format: {version_str}")
        sys.exit(1)
    try:
        return tuple(int(p) for p in parts)
    except ValueError:
        print(f"❌ Error: Version must be numbers: {version_str}")
        sys.exit(1)


def bump_version(current, bump_type):
    """Bump version based on type"""
    major, minor, patch = parse_version(current)

    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        # Assume it's a specific version
        parse_version(bump_type)  # Validate format
        return bump_type


def update_file(file_path, pattern, replacement):
    """Update version in a file"""
    content = Path(file_path).read_text()
    new_content = re.sub(pattern, replacement, content)

    if content == new_content:
        print(f"⚠️  Warning: No changes made to {file_path}")
        return False

    Path(file_path).write_text(new_content)
    return True


def update_version_files(old_version, new_version):
    """Update version in all files"""
    files_updated = []

    # Update tflink/__init__.py
    if update_file(
        "tflink/__init__.py",
        r"__version__ = ['\"][^'\"]+['\"]",
        f"__version__ = '{new_version}'"
    ):
        files_updated.append("tflink/__init__.py")

    # Update pyproject.toml
    if update_file(
        "pyproject.toml",
        r'version = "[^"]+"',
        f'version = "{new_version}"'
    ):
        files_updated.append("pyproject.toml")

    return files_updated


def git_operations(new_version, files_updated):
    """Perform git operations"""
    if not files_updated:
        print("❌ No files were updated")
        return False

    try:
        # Check if git repo
        subprocess.run(['git', 'status'], check=True, capture_output=True)

        print("\n📝 Git operations:")

        # Stage files
        for file in files_updated:
            subprocess.run(['git', 'add', file], check=True)
            print(f"   ✓ Staged: {file}")

        # Create commit
        commit_msg = f"Bump version to {new_version}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        print(f"   ✓ Committed: {commit_msg}")

        # Create tag
        tag_name = f"v{new_version}"
        subprocess.run(['git', 'tag', '-a', tag_name, '-m', f"Release {new_version}"], check=True)
        print(f"   ✓ Tagged: {tag_name}")

        return True

    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git operation failed: {e}")
        print("   You can manually commit the changes.")
        return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py [major|minor|patch|X.Y.Z]")
        print("\nExamples:")
        print("  python bump_version.py patch   # 0.1.0 -> 0.1.1")
        print("  python bump_version.py minor   # 0.1.0 -> 0.2.0")
        print("  python bump_version.py major   # 0.1.0 -> 1.0.0")
        print("  python bump_version.py 0.2.0   # Set to specific version")
        sys.exit(1)

    bump_type = sys.argv[1]

    # Get current version
    current_version = get_current_version()
    print(f"📌 Current version: {current_version}")

    # Calculate new version
    new_version = bump_version(current_version, bump_type)
    print(f"🎯 New version: {new_version}")

    # Confirm
    response = input(f"\n❓ Update version from {current_version} to {new_version}? [y/N]: ")
    if response.lower() != 'y':
        print("❌ Cancelled")
        sys.exit(0)

    # Update files
    print("\n📝 Updating files...")
    files_updated = update_version_files(current_version, new_version)

    if files_updated:
        for file in files_updated:
            print(f"   ✓ Updated: {file}")
    else:
        print("❌ No files were updated")
        sys.exit(1)

    # Git operations
    response = input("\n❓ Create git commit and tag? [Y/n]: ")
    if response.lower() != 'n':
        if git_operations(new_version, files_updated):
            print("\n✅ Version bump complete!")
            print("\n📋 Next steps:")
            print(f"   1. Review changes: git show")
            print(f"   2. Push code: git push")
            print(f"   3. Push tag: git push origin v{new_version}")
            print(f"   4. Create GitHub Release for v{new_version}")
            print(f"   5. GitHub Actions will auto-publish to PyPI!")
        else:
            print("\n⚠️  Version updated but git operations failed")
            print("   You can manually commit and tag:")
            print(f"   git add {' '.join(files_updated)}")
            print(f"   git commit -m 'Bump version to {new_version}'")
            print(f"   git tag -a v{new_version} -m 'Release {new_version}'")
    else:
        print("\n✅ Files updated!")
        print("\n📋 Manual steps:")
        print(f"   git add {' '.join(files_updated)}")
        print(f"   git commit -m 'Bump version to {new_version}'")
        print(f"   git tag -a v{new_version} -m 'Release {new_version}'")
        print(f"   git push && git push origin v{new_version}")


if __name__ == "__main__":
    main()
