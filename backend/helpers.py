import os
import shutil
from git import Repo
import logging

# ------------------------------------------------------------
# Logging Setup for GitReadme
# ------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [GitReadme Helper] - %(levelname)s - %(message)s"
)
logger = logging.getLogger("GitReadmeHelper")


class Helper:

    # ------------------------------------------------------------
    # Extract text/code files recursively from a cloned repo
    # ------------------------------------------------------------
    def extract_code_from_repo(self, folder_name: str) -> str:
        """
        Collect all readable source files from a repo.
        Returns a giant string with "File: <filepath>" headers.
        """
        code_text = ""
        allowed_extensions = {
            ".py", ".md", ".txt", ".json", ".yaml", ".yml", ".csv",
            ".ini", ".cfg", ".xml", ".html", ".js", ".css",
            ".java", ".c", ".cpp", ".ts", ".go", ".rs",
            ".rb", ".php", ".sh", ".bat"
        }

        for root, _, files in os.walk(folder_name):
            for file in files:
                try:
                    path = os.path.join(root, file)
                    _, ext = os.path.splitext(file)

                    # Skip binary / unknown file types
                    if ext.lower() not in allowed_extensions:
                        continue

                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()

                    code_text += f"File: {path}\n{content}\n\n"

                except Exception as e:
                    logger.warning(f"Error reading file {file}: {e}")

        return code_text

    # ------------------------------------------------------------
    # Clone GitHub repo into /projects/<repo_name>
    # ------------------------------------------------------------
    def clone_repo(self, github_url: str, folder_name: str = "cloned_repo") -> str:
        """
        Clone a GitHub repository into /projects/<repo_name>.
        Returns the full path.
        """

        projects_dir = "projects"
        if not os.path.exists(projects_dir):
            os.makedirs(projects_dir)
            logger.info(f"Created directory: {projects_dir}")

        full_path = os.path.join(projects_dir, folder_name)

        if os.path.exists(full_path):
            logger.info(f"Folder '{full_path}' already exists. Using existing clone.")
        else:
            try:
                logger.info(f"Cloning repository: {github_url}")
                Repo.clone_from(github_url, full_path)
                logger.info(f"Repository cloned into: {full_path}")
            except Exception as e:
                logger.error(f"Failed to clone repository: {e}")
                raise

        return full_path

    # ------------------------------------------------------------
    # Cleanup cloned repo
    # ------------------------------------------------------------
    def delete_cloned_repo(self, folder_path: str) -> bool:
        """
        Safely delete a cloned repo folder after the README generation is done.
        """
        try:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                logger.info(f"Deleted folder: {folder_path}")
                return True
            else:
                logger.warning(f"Folder not found: {folder_path}")
                return False

        except PermissionError as e:
            logger.error(f"Permission denied removing {folder_path}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error removing {folder_path}: {e}")
            return False
