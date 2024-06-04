import openai

# Set the OpenAI API key
openai.api_key = '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'

# Path to the dataset file
dataset_file_path = 'finetune_dataset.jsonl'

# Upload the file
uploaded_file = openai.File.create(file=open(dataset_file_path), purpose='fine-tune')

# Create a fine-tuning job with the new file handling
response = openai.FineTun.create(
    training_file=uploaded_file.id,
    model="gpt-4",
    n_epochs=4,  # 원하는 epoch 수
    batch_size=1  # 데이터 크기에 따라 조정
)

# Print the fine-tuning job ID
print("Fine-tune job ID:", response['id'])
