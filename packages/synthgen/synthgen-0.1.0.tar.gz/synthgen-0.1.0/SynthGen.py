import random
import string
import numpy as np
from collections import Counter
import re
import time

# this works!
class SynthGen:
    def __init__(self, seed = None):
        self.seed = seed 
        self.has_run = False
        
    def run_once(self):
        if not self.has_run:
            print("Creating strings...")
            
            # Set the flag to indicate that the method has run
            self.has_run = True
        else:
            print("Method has already run. Skipping further execution.")

    def generate_strings(self, total_strings, unique_percentage,  gender_settings = None, gender_overlap_percentage = 0, ethnicity_settings = None, ethnicity_overlap_percentages= None, string_settings = None):
        """
        Generate a list of strings with a specified level of uniqueness.

        Parameters:
        - unique_percentage (dict): Dictionary specifying percentage of unique strings.
        - total_strings (int): Total number of strings to generate.
        - gender_settings (dict): Dictionary specifying gender proportions.
        - gender_overlap_percentage (int): Percentage of names that overlap between male and female.
        - ethnicity_settings (dict): Dictionary specifying ethnicity proportions.

        Returns:
        - List of generated strings (and genders, ethnicities if specified).
        """
        if not 0 <= unique_percentage <= 1:
            raise ValueError("Unique percentage must be between 0 and 1.")

        unique_counts = {ethnicity: int(total_strings * ethnicity_settings[ethnicity] * unique_percentage) for ethnicity in ethnicity_settings}
        non_unique_counts = {ethnicity: int((total_strings * ethnicity_settings[ethnicity]) - count) for ethnicity, count in unique_counts.items()}
        
        unique_strings = []
        non_unique_strings = []
        
        # unique_strings = [generate_random_string() for _ in range(unique_count)]
        # non_unique_strings = generate_non_unique_strings(non_unique_count, unique_strings)

        for ethnicity in ethnicity_settings:
            ethnicity_unique_strings = [self.generate_random_string(string_settings) for _ in range(unique_counts[ethnicity])]
            unique_strings.extend(ethnicity_unique_strings)
            ethnicity_non_unique_strings = self.generate_non_unique_strings(non_unique_counts[ethnicity], ethnicity_unique_strings)
            non_unique_strings.extend(ethnicity_non_unique_strings)

        if ethnicity_settings and ethnicity_overlap_percentages:
            for (ethnicity1, ethnicity2), overlap_percentage in ethnicity_overlap_percentages.items():
                unique_names_ethnicity1 = set([s for s, e in zip(unique_strings, ethnicity_settings) if e == ethnicity1])
                overlap_count = int(len(unique_names_ethnicity1) * overlap_percentage)

                if overlap_count > 0:
                    overlap_names = random.sample(unique_names_ethnicity1, overlap_count)
                    unique_strings = [self.generate_random_string(string_settings) if s in overlap_names and e == ethnicity2 else s for s, e in zip(unique_strings, ethnicity_settings)]

        all_strings = unique_strings + non_unique_strings
        random.shuffle(all_strings)

        genders = self.generate_genders(total_strings, gender_settings, gender_overlap_percentage, ethnicity_settings, ethnicity_overlap_percentages) if gender_settings and gender_overlap_percentage else self.generate_genders(total_strings, gender_settings)
        adjusted_unique_counts = Counter(ethnicity_settings)

        for ethnicity in ethnicity_settings:
            adjusted_unique_counts[ethnicity] += len([s for s, e in zip(unique_strings, ethnicity_settings) if e == ethnicity])

        if ethnicity_settings:
            ethnicities = self.generate_ethnicities(total_strings, ethnicity_settings)
            strings_with_gender_and_ethnicity = list(zip(all_strings, genders, ethnicities))
            return strings_with_gender_and_ethnicity
        else:
            strings_with_gender = list(zip(all_strings, genders))
            return strings_with_gender
        
    def generate_random_string(self, string_settings = None):
        # Adjust the length distribution based on your requirements
        lengths = string_settings.get('lengths', [4, 5, 6])
        probabilities = string_settings.get('length_probabilities', [0.3, 0.4, 0.3])
        length = random.choices(lengths, weights=probabilities)[0]

        num_terms_range = string_settings.get('num_terms_range', [1, 2, 3])
        num_terms_probabilities = string_settings.get('num_terms_probabilities', [0.2, 0.6, 0.2])
        num_terms = random.choices(num_terms_range, weights=num_terms_probabilities)[0]

        return ' '.join([self._generate_term(length) for _ in range(num_terms)])

    def _generate_term(self, length):
        term = ''.join(random.choices(string.ascii_lowercase, k=length))
        return term

    def generate_non_unique_strings(self, count, unique_strings):
        # Generate non-unique strings based on Zipf distribution
        # Using Zipf distribution parameter (alpha) of 2 for simplicity
        zipf_distribution = np.array([1.0 / i for i in range(1, len(unique_strings) + 1)])
        zipf_distribution /= zipf_distribution.sum()
        non_unique_strings = random.choices(unique_strings, weights=zipf_distribution, k=count)
        return non_unique_strings
        
    def generate_ethnicities(self, count, ethnicity_settings):
        """
        Generate random ethnicity information based on specified proportions.

        Parameters:
        - count (int): Total number of ethnicity values to generate.
        - ethnicity_settings (dict): Dictionary specifying ethnicity proportions.

        Returns:
        - List of randomly generated ethnicity values.
        """
        ethnicities = []
        for ethnicity, proportion in ethnicity_settings.items():
            ethnicity_count = int(count * proportion)
            ethnicities.extend([ethnicity] * ethnicity_count)

        # If the counts don't add up to the total, adjust randomly
        while len(ethnicities) < count:
            ethnicity = random.choice(list(ethnicity_settings.keys()))
            ethnicities.append(ethnicity)

        random.shuffle(ethnicities)
        return ethnicities

    def generate_genders(self, count, gender_settings, gender_overlap_percentage, ethnicity_settings = None, ethnicity_overlap_percentages = None):
        original_gender_counts = {gender: int(count * proportion) for gender, proportion in gender_settings.items()}
        
        # Determine the number of names that should overlap between male and female
        overlap_count = int(count * gender_overlap_percentage)
        updated_gender_counts = {gender: original_gender_counts[gender] + int(overlap_count * gender_settings[gender]) for gender in gender_settings}

        if overlap_count > 0:
            overlap_names = random.sample([gender for gender, count in updated_gender_counts.items() for _ in range(count)], overlap_count)
            updated_gender_counts = {gender: updated_gender_counts[gender] - 1 if gender in overlap_names else updated_gender_counts[gender] for gender in original_gender_counts}
            updated_gender_counts[random.choice(list(gender_settings.keys()))] += overlap_count

        genders = [gender for gender, count in updated_gender_counts.items() for _ in range(count)]

        if ethnicity_settings and ethnicity_overlap_percentages:
            for (ethnicity1, ethnicity2), overlap_percentage in ethnicity_overlap_percentages.items():
                unique_names_ethnicity1 = set([gender for gender, ethnicity in zip(genders, ethnicity_settings) if ethnicity == ethnicity1])
                overlap_count = int(len(unique_names_ethnicity1) * overlap_percentage)

                if overlap_count > 0:
                    overlap_indices = random.sample(range(len(unique_names_ethnicity1)), overlap_count)
                    genders = [g if idx not in overlap_indices or ethnicity != ethnicity2 else self.generate_random_string() for idx, (g, ethnicity) in enumerate(zip(genders, ethnicity_settings))]

        while len(genders) < count:
            gender = random.choice(list(gender_settings.keys()))
            genders.append(gender)

        random.shuffle(genders)
        return genders

"""
    def _calculate_vc_info(self, term):
        vowel_count = len(re.findall('[aeiouAEIOU]', term))
        consonant_count = len(re.findall('[^aeiouAEIOU\s]', term))

        if consonant_count == 0:
            return {'Vowel Count term': vowel_count, 'Consonant Count term': consonant_count, 'Vowel-Consonant Ratio term': float('inf'), 'VC_ratio_cat term': 'undefined'}

        vc_ratio = vowel_count / consonant_count
        vc_ratio_category = self._get_vowel_consonant_ratio_category(vc_ratio)

        return {'Vowel Count term': vowel_count, 'Consonant Count term': consonant_count, 'Vowel-Consonant Ratio term': vc_ratio, 'VC_ratio_cat term': vc_ratio_category}

    def _replace_consonant_with_vowel(self, term):
        consonants = re.findall('[^aeiouAEIOU\s]', term)
        if consonants:
            random_consonant = random.choice(consonants)
            random_vowel = random.choice('aeiouAEIOU')
            term = term.replace(random_consonant, random_vowel, 1)
        return term

    def _replace_vowel_with_consonant(self, term):
        vowels = re.findall('[aeiouAEIOU]', term)
        if vowels:
            random_vowel = random.choice(vowels)
            random_consonant = random.choice([c for c in string.ascii_lowercase if c not in 'aeiouAEIOU'])
            term = term.replace(random_vowel, random_consonant, 1)
        return term

    def _get_vowel_consonant_ratio_category(self, ratio):
        if ratio < 0.5:
            return "low"
        elif ratio < 1:
            return "moderate"
        else:
            return "high"
  """  


# Example usage
seed_value = 42

string_generator = SynthGen(seed = seed_value )  # Create an instance of SynthGen
total_strings = 10000000
unique_percentage = 0.5
gender_settings = {'Male': 0.4, 'Female': 0.6}
gender_overlap_percentage = 0.15
ethnicity_settings = {'White': 0.81, 'Asian': 0.096, 'Black': 0.042, 'Mixed': 0.03, 'Other': 0.022}
ethnicity_overlap_percentages = {('White', 'Black'): 0.1, ('White', 'Asian'): 0.05, ('White', 'Other'): 0.1}

string_settings = {
    'lengths': [4, 5, 6, 7],  # Specify lengths
    'length_probabilities': [0.15, 0.3, 0.4, 0.15],  # Specify length probabilities
    'num_terms_range': [1, 2, 3],  # Specify number of terms range
    'num_terms_probabilities': [0.2, 0.6, 0.2]  # Specify number of terms probabilities
}


# Call the generate_strings method on the instance
start_time = time.time()
generated_strings = string_generator.generate_strings(total_strings,unique_percentage, gender_settings, gender_overlap_percentage, ethnicity_settings, ethnicity_overlap_percentages, string_settings)
end_time = time.time()
execution_time = end_time - start_time

# Assuming you have generated_strings already
unique_counts = Counter(generated_strings)


# Sort by frequency in descending order
sorted_unique_counts = unique_counts.most_common()

# Print or use the counts as needed
# for value, count in sorted_unique_counts:
#    print(f"{value}: {count} occurrences")


# Check the percentage of males and females
gender_counts = Counter([gender for _, gender, _ in generated_strings])
total_count = len(generated_strings)

male_percentage = (gender_counts['Male'] / total_count) * 100
female_percentage = (gender_counts['Female'] / total_count) * 100

print(f"Percentage of Males: {male_percentage:.2f}%")
print(f"Percentage of Females: {female_percentage:.2f}%")

# Check the percentage of people from different ethnicities
ethnicity_counts = Counter([ethnicity for _, _, ethnicity in generated_strings])

for ethnicity, count in ethnicity_counts.items():
    ethnicity_percentage = (count / total_count) * 100
    print(f"Percentage of {ethnicity}: {ethnicity_percentage:.2f}%")

# Calculate the count of unique names for each ethnicity
unique_names_by_ethnicity = {}
for ethnicity in set([ethnicity for _, _, ethnicity in generated_strings]):
    unique_names_count = len(set([name for name, _, e in generated_strings if e == ethnicity]))
    unique_names_by_ethnicity[ethnicity] = unique_names_count

# Print the percentage of unique names for each ethnicity
for ethnicity, unique_count in unique_names_by_ethnicity.items():
    total_count = ethnicity_counts[ethnicity]
    unique_percentage = (unique_count / total_count) * 100
    print(f"Number of Unique Names in {ethnicity}: {unique_count}")
    print(f"Percentage of Unique Names in {ethnicity}: {unique_percentage:.2f}%")

print(f"Time taken to generate strings: {execution_time:.2f} seconds")
