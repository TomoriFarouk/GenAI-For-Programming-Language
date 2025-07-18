# model-training/requirements.txt
from tqdm import tqdm
import logging
from typing import Dict, List, Any, Optional
from datasets import load_dataset, Dataset, DatasetDict
import pandas as pd
import json
import os
datasets == 2.14.0
transformers == 4.36.0
torch == 2.1.0
pandas == 2.0.3
numpy == 1.24.3
huggingface_hub == 0.19.0
tqdm == 4.66.0
jupyter == 1.0.0
matplotlib == 3.7.2
seaborn == 0.12.2

# model-training/scripts/data_preparation.py

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreparator:
    """Unified data preparation for multiple programming datasets"""

    def __init__(self, output_dir: str = "data/unified"):
        self.output_dir = output_dir
        self.datasets_config = {
            'code_feedback': {
                'name': 'code_feedback',
                'type': 'feedback',
                'languages': ['python', 'java', 'javascript']
            },
            'codealpaca': {
                'name': 'codealpaca',
                'type': 'instruction',
                'languages': ['python', 'java', 'javascript']
            },
            'apps': {
                'name': 'codeparrot/apps',
                'type': 'problems',
                'languages': ['python']
            },
            'mbpp': {
                'name': 'mbpp',
                'type': 'problems',
                'languages': ['python']
            },
            'code_contests': {
                'name': 'deepmind/code_contests',
                'type': 'contests',
                'languages': ['python', 'java', 'javascript']
            }
        }

        os.makedirs(output_dir, exist_ok=True)

    def load_datasets(self) -> Dict[str, Any]:
        """Load all datasets from HuggingFace"""
        loaded_datasets = {}

        for key, config in self.datasets_config.items():
            try:
                logger.info(f"Loading {config['name']}...")
                dataset = load_dataset(config['name'])
                loaded_datasets[key] = {
                    'dataset': dataset,
                    'config': config
                }
                logger.info(f"Loaded {config['name']} successfully")
            except Exception as e:
                logger.error(f"Failed to load {config['name']}: {e}")
                continue

        return loaded_datasets

    def create_unified_format(self, datasets: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert all datasets to unified format"""
        unified_data = []

        for dataset_key, dataset_info in datasets.items():
            logger.info(f"Processing {dataset_key}...")

            dataset = dataset_info['dataset']
            config = dataset_info['config']

            if config['type'] == 'feedback':
                unified_data.extend(
                    self._process_feedback_dataset(dataset, dataset_key))
            elif config['type'] == 'instruction':
                unified_data.extend(
                    self._process_instruction_dataset(dataset, dataset_key))
            elif config['type'] == 'problems':
                unified_data.extend(
                    self._process_problems_dataset(dataset, dataset_key))
            elif config['type'] == 'contests':
                unified_data.extend(
                    self._process_contests_dataset(dataset, dataset_key))

        logger.info(f"Created {len(unified_data)} unified training examples")
        return unified_data

    def _process_feedback_dataset(self, dataset, source: str) -> List[Dict[str, Any]]:
        """Process code feedback datasets"""
        processed = []

        # Assuming dataset has 'train' split
        for item in tqdm(dataset['train'], desc=f"Processing {source}"):
            try:
                # Adapt based on actual dataset structure
                processed_item = {
                    'input': {
                        'code': item.get('code', ''),
                        'language': self._detect_language(item.get('code', '')),
                        'assignment_context': item.get('problem_description', ''),
                        'feedback_type': 'general',
                        'student_level': 'intermediate'
                    },
                    'output': {
                        'overall_score': item.get('score', 75.0),
                        'feedback_categories': {
                            'correctness': item.get('correctness_feedback', ''),
                            'style': item.get('style_feedback', ''),
                            'efficiency': item.get('efficiency_feedback', ''),
                            'best_practices': item.get('best_practices_feedback', ''),
                            'debugging': item.get('debugging_feedback', '')
                        },
                        'specific_suggestions': self._extract_suggestions(item),
                        'summary': item.get('overall_feedback', ''),
                        'strengths': item.get('strengths', []),
                        'areas_for_improvement': item.get('improvements', [])
                    },
                    'source': source
                }
                processed.append(processed_item)
            except Exception as e:
                logger.warning(f"Skipped item in {source}: {e}")
                continue

        return processed

    def _process_instruction_dataset(self, dataset, source: str) -> List[Dict[str, Any]]:
        """Process instruction-following datasets like CodeAlpaca"""
        processed = []

        for item in tqdm(dataset['train'], desc=f"Processing {source}"):
            try:
                # Extract code from instruction-output pair
                instruction = item.get('instruction', '')
                code_output = item.get('output', '')

                processed_item = {
                    'input': {
                        'code': code_output,
                        'language': self._detect_language(code_output),
                        'assignment_context': instruction,
                        'feedback_type': 'general',
                        'student_level': 'intermediate'
                    },
                    'output': {
                        'overall_score': 85.0,  # Default for instruction datasets
                        'feedback_categories': {
                            'correctness': 'Code correctly implements the requested functionality',
                            'style': 'Good code structure and naming',
                            'efficiency': 'Reasonable algorithmic approach',
                            'best_practices': 'Follows standard programming practices',
                            'debugging': None
                        },
                        'specific_suggestions': [],
                        'summary': f'Well-implemented solution for: {instruction[:100]}...',
                        'strengths': ['Clear implementation', 'Addresses requirements'],
                        'areas_for_improvement': ['Consider edge cases', 'Add error handling']
                    },
                    'source': source
                }
                processed.append(processed_item)
            except Exception as e:
                logger.warning(f"Skipped item in {source}: {e}")
                continue

        return processed

    def _process_problems_dataset(self, dataset, source: str) -> List[Dict[str, Any]]:
        """Process programming problems datasets"""
        processed = []

        for item in tqdm(dataset['train'], desc=f"Processing {source}"):
            try:
                problem_text = item.get('text', '') or item.get(
                    'problem_description', '')
                code_solution = item.get(
                    'code', '') or item.get('solution', '')

                if not code_solution:
                    continue

                processed_item = {
                    'input': {
                        'code': code_solution,
                        'language': self._detect_language(code_solution),
                        'assignment_context': problem_text,
                        'feedback_type': 'algorithm',
                        'student_level': 'intermediate'
                    },
                    'output': {
                        'overall_score': 90.0,  # High score for correct solutions
                        'feedback_categories': {
                            'correctness': 'Solution correctly solves the problem',
                            'style': 'Clean and readable code structure',
                            'efficiency': 'Efficient algorithmic approach',
                            'best_practices': 'Good use of language features',
                            'debugging': None
                        },
                        'specific_suggestions': [],
                        'summary': 'Effective solution with good algorithm design',
                        'strengths': ['Correct logic', 'Good algorithm choice'],
                        'areas_for_improvement': ['Consider alternative approaches']
                    },
                    'source': source
                }
                processed.append(processed_item)
            except Exception as e:
                logger.warning(f"Skipped item in {source}: {e}")
                continue

        return processed

    def _process_contests_dataset(self, dataset, source: str) -> List[Dict[str, Any]]:
        """Process competitive programming datasets"""
        processed = []

        # Similar to problems dataset but with competitive programming context
        for item in tqdm(dataset['train'], desc=f"Processing {source}"):
            try:
                problem = item.get('description', '')
                solutions = item.get('solutions', {})

                # Process each solution
                for lang, code in solutions.items():
                    if lang in ['python', 'java', 'javascript'] and code:
                        processed_item = {
                            'input': {
                                'code': code,
                                'language': lang,
                                'assignment_context': problem,
                                'feedback_type': 'algorithm',
                                'student_level': 'advanced'
                            },
                            'output': {
                                'overall_score': 95.0,  # Very high for contest solutions
                                'feedback_categories': {
                                    'correctness': 'Optimal solution for competitive programming',
                                    'style': 'Efficient competitive programming style',
                                    'efficiency': 'Highly optimized algorithm',
                                    'best_practices': 'Contest-appropriate coding practices',
                                    'debugging': None
                                },
                                'specific_suggestions': [],
                                'summary': 'Excellent competitive programming solution',
                                'strengths': ['Optimal complexity', 'Contest-ready'],
                                'areas_for_improvement': ['Add comments for readability']
                            },
                            'source': source
                        }
                        processed.append(processed_item)
            except Exception as e:
                logger.warning(f"Skipped item in {source}: {e}")
                continue

        return processed

    def _detect_language(self, code: str) -> str:
        """Simple language detection based on code patterns"""
        code_lower = code.lower()

        # Python indicators
        if any(keyword in code for keyword in ['def ', 'import ', 'print(', 'if __name__']):
            return 'python'

        # Java indicators
        if any(keyword in code for keyword in ['public class', 'public static void main', 'System.out']):
            return 'java'

        # JavaScript indicators
        if any(keyword in code for keyword in ['function ', 'const ', 'let ', 'console.log']):
            return 'javascript'

        return 'python'  # Default fallback

    def _extract_suggestions(self, item: Dict) -> List[Dict[str, Any]]:
        """Extract specific suggestions from feedback item"""
        suggestions = []

        # This would depend on the actual dataset structure
        if 'suggestions' in item:
            for sugg in item['suggestions']:
                suggestions.append({
                    'line_number': sugg.get('line_number'),
                    'issue_type': sugg.get('type', 'general'),
                    'description': sugg.get('description', ''),
                    'suggestion': sugg.get('suggestion', ''),
                    'severity': sugg.get('severity', 'medium')
                })

        return suggestions

    def create_training_prompts(self, unified_data: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Convert unified data to training prompts"""
        training_data = []

        for item in tqdm(unified_data, desc="Creating training prompts"):
            try:
                # Create input prompt
                input_data = item['input']
                output_data = item['output']

                prompt = f"""You are an expert programming instructor providing constructive feedback on student code.

**Student Code ({input_data['language']}):**
```{input_data['language']}
{input_data['code']}
```

**Assignment Context:** {input_data['assignment_context']}
**Student Level:** {input_data['student_level']}
**Feedback Focus:** {input_data['feedback_type']}

Please provide comprehensive feedback in JSON format with the following structure:
- overall_score: score from 0-100
- feedback_categories: correctness, style, efficiency, best_practices, debugging
- specific_suggestions: array of specific improvement suggestions
- summary: brief summary of key points
- strengths: array of code strengths
- areas_for_improvement: array of improvement areas

Focus on being constructive, educational, and encouraging."""

                # Create expected response
                response = json.dumps(output_data, indent=2)

                training_data.append({
                    'prompt': prompt,
                    'response': response,
                    'source': item['source']
                })

            except Exception as e:
                logger.warning(f"Failed to create prompt: {e}")
                continue

        return training_data

    def save_processed_data(self, training_data: List[Dict[str, str]]):
        """Save processed data for training"""

        # Save as JSON
        output_file = os.path.join(self.output_dir, 'training_data.json')
        with open(output_file, 'w') as f:
            json.dump(training_data, f, indent=2)

        # Save as HuggingFace dataset
        dataset = Dataset.from_pandas(pd.DataFrame(training_data))
        dataset.save_to_disk(os.path.join(self.output_dir, 'hf_dataset'))

        # Create train/validation split
        split_dataset = dataset.train_test_split(test_size=0.1, seed=42)

        dataset_dict = DatasetDict({
            'train': split_dataset['train'],
            'validation': split_dataset['test']
        })

        dataset_dict.save_to_disk(os.path.join(
            self.output_dir, 'hf_dataset_split'))

        logger.info(
            f"Saved {len(training_data)} training examples to {self.output_dir}")
        logger.info(f"Train split: {len(split_dataset['train'])} examples")
        logger.info(f"Validation split: {len(split_dataset['test'])} examples")

    def run_full_pipeline(self):
        """Run the complete data preparation pipeline"""
        logger.info("Starting data preparation pipeline...")

        # Load datasets
        datasets = self.load_datasets()

        # Create unified format
        unified_data = self.create_unified_format(datasets)

        # Create training prompts
        training_data = self.create_training_prompts(unified_data)

        # Save processed data
        self.save_processed_data(training_data)

        logger.info("Data preparation pipeline completed!")

        return {
            'total_examples': len(training_data),
            'sources': list(set([item['source'] for item in training_data])),
            'output_dir': self.output_dir
        }


if __name__ == "__main__":
    preparator = DataPreparator()
    results = preparator.run_full_pipeline()
    print(f"Pipeline completed: {results}")
