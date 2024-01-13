import string
import os

# Constants for keys
VALID_KEYS = set(
    [
        "last_name",
        "first_name",
        "org",
        "title",
        "phone",
        "email",
        "website",
        "street",
        "city",
        "p_code",
        "country",
    ]
)


def vcf_card_generate(df, d, prefix=None, path=None):
    """
    Generates vCards based on the provided DataFrame and dictionary of column mappings.
    df: DataFrame with contact information
    d: Dictionary of column mappings
    prefix: Prefix to be added to first names
    path: Path to save the vCard file
    """

    # Preprocessing
    df2 = df.copy()
    df2 = parse_data(df2, d)
    df2 = treat_phone(df2, "phone")
    df2 = treat_name(df2, "last_name")
    df2 = treat_name(df2, "first_name")
    df2 = to_add_prefix(df2, prefix)

    # Vcard Generation
    bulk_create_vcard(df2, path)


def parse_data(df, d):
    """
    Parses the DataFrame based on the provided column mappings.
    df: DataFrame with contact information
    d: Dictionary of column mappings

    raise exeption if d.keys duplicate, d.keys not in  sorted_format_columns, and d.values duplicate
    """

    # Validation checks
    validate_column_mappings(d)

    selected_column_list = [value for value in d.values() if value is not None]
    df2 = df[selected_column_list].copy()

    sorted_format_columns = list(VALID_KEYS)
    for key_col in sorted_format_columns:
        if key_col in d.keys():
            try:
                df2 = df2.rename(columns={d[key_col]: key_col})
            except Exception as e:
                print(e)
        else:
            df2[key_col] = ""

    df2 = df2[sorted_format_columns]
    return df2


def validate_column_mappings(d):
    """
    Validates the column mappings dictionary.
    """
    if len(set(d.keys())) < len(d.keys()):
        raise ValueError(
            "Duplicate keys found in parsed data dictionary. Each key should be unique."
        )

    if not set(d.keys()).issubset(VALID_KEYS):
        raise ValueError(
            f"Invalid keys found in parsed data dictionary. Keys should be a subset of {VALID_KEYS}."
        )

    if len(set(d.values())) < len(d.values()):
        raise ValueError(
            "Duplicate values found in parsed data dictionary. Each value should be unique."
        )


def treat_phone(df, phone):
    """
    Cleans and formats phone numbers in the DataFrame.
    df: DataFrame with contact information
    phone: Name of the phone column
    """
    df[phone] = df[phone].astype(str)
    df[phone] = df[phone].str.replace(" ", "")
    df[phone] = df[phone].replace(r"\.\d+", "", regex=True)
    df[phone] = df[phone].replace(r"[^\w\s]", "", regex=True)
    df[phone] = df.apply(
        lambda x: x[phone][1:] if (x[phone].startswith("++")) else x[phone], axis=1
    )
    df[phone] = df.apply(
        lambda x: x[phone][2:] if (x[phone].startswith("+601")) else x[phone], axis=1
    )
    df[phone] = df.apply(
        lambda x: x[phone][1:] if (x[phone].startswith("601")) else x[phone], axis=1
    )

    df[phone] = df.apply(
        lambda x: f"{x[phone][:-2]}" if (x[phone].endswith(".0")) else x[phone], axis=1
    )
    return df


def treat_name(df, name):
    """
    Cleans and formats names in the DataFrame.
    df: DataFrame with contact information
    name: Name of the column containing names
    """
    df[name] = df[name].str.strip()
    df[name] = df[name].str.replace("\d+", "", regex=True)
    df[name] = df.apply(
        lambda x: x[name].translate(str.maketrans("", "", string.punctuation)), axis=1
    )
    df[name] = df.apply(lambda x: x[name].title(), axis=1)
    df[name] = df.apply(lambda x: x[name].replace("  ", " "), axis=1)
    return df


def to_add_prefix(df, prefix):
    """
    Adds a prefix to first names in the DataFrame.
    df: DataFrame with contact information
    prefix: Prefix to be added
    """
    df["first_name"] = df.apply(lambda x: f"{prefix}{x['first_name']}", axis=1)
    return df


def create_vcard(contact: dict):
    """
    The mappings used below are from https://www.w3.org/TR/vcard-rdf/#Mapping
    """
    vc_begin = "BEGIN:VCARD\n"
    vc_version = "VERSION:3.0\n"
    vc_name = f"N;CHARSET=UTF-8:{contact['last_name']};{contact['first_name']};;;\n"
    vc_title = f"TITLE;CHARSET=UTF-8:{contact['title']}\n"
    vc_org = f"ORG;CHARSET=UTF-8:{contact['org']}\n"
    vc_phone = f"TEL;TYPE=WORK,VOICE:{contact['phone']}\n"
    vc_email = f"EMAIL;TYPE=WORK:{contact['email']}\n"
    vc_website = f"URL;TYPE=WORK:{contact['website']}\n"
    vc_address = f"ADR;TYPE=WORK;CHARSET=UTF-8:{contact['street']};{contact['city']};{contact['p_code']};{contact['country']}\n"
    vc_end = "END:VCARD\n"

    vc_filename = f"{contact['last_name'].lower()}_{contact['first_name'].lower()}.vcf"
    vc_output = (
        vc_begin
        + vc_version
        + vc_name
        + vc_title
        + vc_org
        + vc_phone
        + vc_email
        + vc_website
        + vc_address
        + vc_end
    )

    vc_final = {
        "filename": vc_filename,
        "output": vc_output,
        "name": contact["first_name"] + contact["last_name"],
    }

    return vc_final


def bulk_create_vcard(df2, path):
    """
    Generate vCard files from a DataFrame of contact information and write them to a specified file.

    Parameters:
    - df2 (pd.DataFrame): DataFrame containing contact information.
    - path (str): File path to save the vCard entries.

    Raises:
    - IsADirectoryError: If the specified path is a directory.
    - ValueError: If the file name doesn't end with '.vcf'.

    If 'path' is not provided, the default file name is 'result.vcf'. The function iterates over
    each contact in the DataFrame, creates vCard entries using the 'create_vcard' function, and writes
    them to the specified file. Prints a message indicating the successful vCard generation.
    """

    parsed_contacts = df2.to_dict(orient="records")

    if not path:
        path = "result.vcf"
        
    if os.path.isdir(path):
        raise IsADirectoryError(
            f"{path} is a directory. Specify a valid file path ending with '.vcf'."
        )

    if not path.lower().endswith(".vcf"):
        raise ValueError(
            "The vCard file name must end with '.vcf'. Please provide a valid file path."
        )


    with open(path, "w", encoding="utf-8") as vcf_file:
        for contact in parsed_contacts:
            vcard_dict = create_vcard(contact)
            vcard = vcard_dict["output"]

            # Append the vCard to the file
            vcf_file.write(vcard + "\n")
    print(f"Generated vcard. {len(df2)} of them. At {path}")
