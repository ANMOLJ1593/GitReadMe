from gitreadme_brain import GitReadmeBrain   # ✅ renamed
from helpers import Helper
from generators import Generators
import os

class ReadmeGeneratorApp:
    """
    Main application wrapper for GitReadme.
    Handles:
    - Repo cloning
    - Code extraction
    - LLM summarization
    - README generation
    - Optional vectorstore examples
    """

    def __init__(self):
        # Core engine components
        self.brain = GitReadmeBrain()          # ✅ uses OpenAI now
        self.helper = Helper()
        self.generator = Generators()

        # Initialize LLM + embeddings
        self.llm = self.brain.getLLM()
        self.embeddings = self.brain.getEmbeddingModel()

    def generate_readme_from_repo_url(self, github_url: str, generator_method: str = "Standard README"):
        """
        Main function to create a README for a GitHub repo.
        Download repo → Parse code → Summarize → Generate README
        """

        # Extract repo name from URL
        repo_name = github_url.rstrip('/').split('/')[-1]

        # Clone repo
        local_path = self.helper.clone_repo(github_url, repo_name)

        # Extract code
        code_text = self.helper.extract_code_from_repo(local_path)

        # Summarize project codebase
        summary = self.generator.summarize_code(self.llm, code_text)

        # Choose README generation method
        if generator_method == "Standard README":
            readme_content = self.generator.generate_readme(self.llm, summary)

        elif generator_method == "README with Examples":
            readme_content = self.generator.generate_readme_with_examples_vectorstore(
                self.llm,
                self.embeddings,
                summary
            )

        else:
            raise ValueError(f"Unknown generator method: {generator_method}")

        # Save generated README inside repo folder
        output_path = os.path.join(local_path, "GENERATED_README.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

        print(f"\n✅ README generated at: {output_path}\n")
        print("🔍 Preview:")
        print("-" * 60)
        print(readme_content[:1000])  # Show preview in console

        # Cleanup the repo folder
        cleanup_success = self.helper.delete_cloned_repo(local_path)
        if cleanup_success:
            print("🧹 Cleanup completed successfully")
        else:
            print("⚠️ Warning: Could not clean up temporary files")

        return readme_content
