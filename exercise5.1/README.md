## FIXED PARTS

- **Fixed print of Rogue version**  
  - Old:  
    ```python
    print("Rouge Score version:", rouge-score.__version__)
    ```  
  - New:  
    ```python
    print("Rouge Score version:", importlib.metadata.version('rouge-score'))
    ```
- **Changed parameters:**  
  - `max_steps = 500`
  - `logging_steps = 50`
  - `eval_steps = 50`
 
## Hugging Face

- https://huggingface.co/Suomenlahti/phi-2-dialogsum-finetuned
![image](https://github.com/user-attachments/assets/5af1a9ad-254c-4cb9-b030-48fea8f103d4)

## Evaluation

**Original model:**  
```json
{
  "rouge1": 0.2999,
  "rouge2": 0.1020,
  "rougeL": 0.2076,
  "rougeLsum": 0.2192
}
```

**PEFT MODEL**
```json
{
  "rouge1": 0.3277,
  "rouge2": 0.0860,
  "rougeL": 0.2297,
  "rougeLsum": 0.2519
}
```

**Absolute percentage improvement of PEFT MODEL over ORIGINAL MODEL**
```json
{
  "rouge1": "2.79%",
  "rouge2": "-1.60%",
  "rougeL": "2.21%",
  "rougeLsum": "3.26%"
}
```
