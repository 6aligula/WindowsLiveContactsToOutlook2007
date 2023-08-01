import pandas as pd

class ContactManager:

    def __init__(self, filepath, encoding='latin1'):
        self.filepath = filepath
        self.encoding = encoding
        self.df = pd.read_csv(filepath, encoding=encoding)

    def add_line(self, data):
        new_row = ["" for _ in range(len(self.df.columns))]  
        for position, value in data.items():
            new_row[position] = value
        self.df.loc[len(self.df)] = new_row  
    
    def correct_accents_and_lower_emails(self, name_col, email_col):
        self.df[name_col] = self.df[name_col].str.encode('latin1').str.decode('utf-8', 'ignore')
        self.df[email_col] = self.df[email_col].str.lower()

    def save(self, filepath):
        self.df.to_csv(filepath, index=False, encoding=self.encoding)


class ContactImporter:

    def __init__(self, filepath, delimiter=',', encoding='latin1'):
        self.filepath = filepath
        self.delimiter = delimiter
        self.encoding = encoding
        self.df = pd.read_csv(filepath, delimiter=delimiter, encoding=encoding)

    def export_data(self, columns):
        return {i: self.df.iloc[i, column] for i in range(len(self.df)) for column in columns}


# Load and manage the original contacts
contact_manager = ContactManager("/mnt/data/mycontacts.csv")

# Import and transform the new contacts
contact_importer = ContactImporter("/mnt/data/contactoswindowslive.csv", delimiter=';')
new_data = contact_importer.export_data(columns=[3, 18, 4])

# Add the new contacts to the original list
contact_manager.add_line(new_data)

# Correct accents and email case
contact_manager.correct_accents_and_lower_emails(name_col=1, email_col=57)

# Save the updated contacts
contact_manager.save("/mnt/data/mycontacts_merged_corrected.csv")
