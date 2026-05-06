# AgenticJarvisCodeBot
An Agentic coding bot built to help fix programming errors and give hilariously sarcastic answers to basic questions.

AI agent can accomplish tasks by calling functions to read files, list files and directories, write and overwrite files, and run python files.
If the user asks a question that doesn't require function calls it simply answers based on Gemini 2.5s LLM response.
If the user asks for something that it knows it cannot accomplish, its "personality" has been set to give hilariously sarcastic responses.

**WARNING** "Jarvis" is made to be a coding assistant, and is hard coded to use a certain, safe, working directory, if downloaded on used on your system without updating and giving him a new safe working directory, the ability to overwrite files and run python code could be potentially dangerous to system operations
