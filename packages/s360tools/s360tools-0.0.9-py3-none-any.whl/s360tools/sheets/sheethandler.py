import gspread
import gspread_formatting
import openpyxl.utils
import pandas as pd
import numpy as np
import typing
from google.colab import auth
import google.auth

def authorize_oauth1() -> gspread.client.Client:
    auth.authenticate_user()
    credentials, _ = google.auth.default(
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets", # Allow access to spreadsheets
            "https://www.googleapis.com/auth/drive"         # Allow access to google drives
        ]
    )
    google_client = gspread.authorize(credentials)
    return google_client

 
class SheetHandler:
    """
    Wrapper object for ease of interacting with the gspread sheet api
    """
    def __init__(self, client: gspread.Client, *, sheet_url: str = "", sheet_id: str = "") -> None:
        """
        Initializes the connection to the sheet using the supplied client
        You must supply either the sheet url or the sheet id
        Arguments:
            client (gspread.Client): The Authorized gspread client to connect to the sheet with
            sheet_url (str) [Optional]: The url for the sheet
            sheet_id (str) [Optional]: The id of the sheet (also called the key)
        """
        if sheet_url != "":
            self.sheet_connection = client.open_by_url(sheet_url)
        elif sheet_id != "":
            self.sheet_connection = client.open_by_key(sheet_id)
        else:
            raise ValueError("Please supply either the sheet url or the sheet id")
        
        self.refresh()

    def refresh(self) -> None:
        self.url = self.sheet_connection.url
        self.id = self.sheet_connection.id
        self.title = self.sheet_connection.title
        self.worksheets = {sheet.title: sheet for sheet in self.sheet_connection.worksheets()}

    def update_title(self, new_title: str) -> None:
        self.sheet_connection.update_title(new_title)
        self.title = self.sheet_connection.title

    def get_worksheet(self, sheet_name: str) -> gspread.Worksheet:
        """
        Gets a worksheet by their name (title)
        Arguments:
            sheet_name (str): The name of the worksheet to fetch
        Returns:
            (gspread.Worksheet): The worksheet with that name
        """
        try:
            return self.worksheets[sheet_name]
        except KeyError:
            raise gspread.WorksheetNotFound(f"The worksheet '{sheet_name}' does not exist in the spreadsheet")
    
    def _check_sheet_input(self, sheet: str | gspread.Worksheet) -> gspread.Worksheet:
        """
        Check if the supplied worksheet is referenced to via name or directly. Converts from name to direct if necessary
        Returns:
            (gspread.Worksheet): The referenced worksheet
        """
        if isinstance(sheet, str):
            sheet = self.get_worksheet(sheet)
        return sheet

    def clear_worksheet(self, sheet: str | gspread.Worksheet, top: int = 1) -> None:
        """
        Clears the worksheet of all data below and including the top row
        Arguments:
            sheet (str | gspread.Worksheet): The sheet to clear
            top (int): The row to start deletion from (1-indexed)
        """
        self._check_sheet_input(sheet).batch_clear([f"A{top}:ZZZ"])   # ZZZ is the maximum column
    
    def sheet_to_dataframe(self, sheet: str  | gspread.Worksheet, head: int = 1, multi_index: bool = False) -> pd.DataFrame:
        """
        Grabs the data from a worksheet and converts it to a pandas dataframe
        Arguments:
            sheet (str | gspread.Worksheet): The worksheet to convert to a dataframe
            head (int): The row index of the header (1-indexed)
            multi_index (bool): Flag for if the header of worksheet utilizes multi-indexing (2-row header)
        Returns:
            (pandas.DataFrame): A dataframe containing the data from the sheet
        """
        sheet_data = self._check_sheet_input(sheet).get_all_values()[head-1:]
        header = sheet_data.pop(0)

        if multi_index:
            sub_header = sheet_data.pop(0)
            super_header = ""
            for i in range(len(sub_header)):
                if header[i] != "":
                    super_header = header[i]
                header[i] = super_header
            header = [np.array(header), np.array(sub_header)]

        frame = pd.DataFrame(sheet_data, columns=header)
        return frame
    
    def dataframe_to_sheet(self, dataframe: pd.DataFrame, sheet: str | gspread.Worksheet, head: int = 1, multi_index: bool = False) -> None:
        """
        Writes a pandas dataframe into a worksheet
        Arguments:
            dataframe (pandas.DataFrame): The dataframe to write to the worksheet
            sheet (str  | gspread.Worksheet): The sheet to write to. Creates a new one if the name does not exist
            head (int): The row in the worksheet to start writing on (1-indexed)
            multi_index (bool): Flag for if the header of dataframe utilizes multi-indexing (2-row header)
        """
        if isinstance(sheet, str) and (sheet not in self.worksheets.keys()):
            rows = head + len(dataframe) + int(multi_index)
            cols = len(dataframe.columns)
            self.create_new_worksheet(sheet, rows, cols)
        sheet = self._check_sheet_input(sheet)

        if multi_index:
            header = list(zip(*dataframe.columns.tolist()))
            header = [list(sub) for sub in header]
            s_head = ""
            for i in range(len(header[0])):
                if header[0][i] == s_head:
                    header[0][i] = ""
                else:
                    s_head = header[0][i]
        else:
            header = [dataframe.columns.tolist()]

        columns = ("A", self._get_letter_index(len(dataframe.columns)))
        rows = (head, head+len(header)+len(dataframe)-1)
        data_cells = f"{columns[0]}{rows[0]}:{columns[1]}{rows[1]}"

        data = dataframe.values.tolist()
        content = header + data
        
        sheet.update(data_cells, content)
    
    def create_new_worksheet(self, sheet_name: str, rows: int = 20000, cols: int = 100) -> gspread.Worksheet:
        """
        Adds a new worksheet to the spreadsheet
        Arguments:
            sheet_name (str): The name of the sheet to add
            rows (int): The number of rows to create
            cols (int): The number of columns to create
        Returns:
            (gspread.Worksheet): The new worksheet
        """
        if sheet_name in self.worksheets.keys():
            raise KeyError(f"A sheet with the name '{sheet_name}' already exists")
        sheet = self.sheet_connection.add_worksheet(sheet_name, rows, cols)
        self.worksheets[sheet_name] = sheet
        return sheet
    
    def delete_worksheet(self, sheet: str | gspread.Worksheet) -> None:
        """
        Removes a worksheet from the spreadsheet
        Arguments:
            sheet (str | gspread.Worksheet): The sheet to remove
        """
        sheet = self._check_sheet_input(sheet)
        self.sheet_connection.del_worksheet(sheet)
        del self.worksheets[sheet.title]
    
    def format_columns_as_boolean(self, sheet: str | gspread.Worksheet, column_index: int, top: int) -> None:
        """
        Format a column as checkboxes
        Arguments:
            sheet (str | gspread.Worksheet): The sheet to format in
            column_index (int): The index of the column to format (1-indexed)
            top (int): The row to start the formatting from (1-indexed)
        """
        validation_rule = gspread_formatting.DataValidationRule(
            gspread_formatting.BooleanCondition("BOOLEAN", []), # condition 'type' and 'values', defaulting to TRUE/FALSE
            showCustomUi = True
        )
        column_letter = self._get_letter_index(column_index-1)
        sheet = self._check_sheet_input(sheet)

        cells = f"{column_letter}{top+1}:{column_letter}"
        gspread_formatting.set_data_validation_for_cell_range(sheet, cells, validation_rule)
    
    def copy_sheet(self, source_sheet: str | gspread.Worksheet, copy_sheet_name: str | gspread.Worksheet) -> gspread.Worksheet:
        """
        Creates a copy of a worksheet in the spreadsheet
        Arguments:
            source_sheet (str | gspread.Worksheet): The worksheet to copy
            copy_sheet_name (str): The name of the sheet to copy to
        Returns:
            (gspread.Worksheet): The copy of the worksheet
        """
        source = self._check_sheet_input(source_sheet)
        copy = self.sheet_connection.duplicate_sheet(source.id, new_sheet_name=copy_sheet_name)

        self.worksheets[copy_sheet_name] = copy
        return copy
    
    def update_sheet_title(self, sheet: str | gspread.Worksheet, new_title: str) -> None:
        """
        Changes the title of worksheet
        Arguments:
            sheet (str | gspread.Worksheet): The worksheet to change the name of
            new_title (str): The new title of the worksheet
        """
        sheet = self._check_sheet_input(sheet)
        del self.worksheets[sheet.title]

        sheet.update_title(new_title)
        self.worksheets[new_title] = sheet

    @staticmethod
    def _get_letter_index(column_index: int) -> str:
        """
        Converts an integer to the corrosponding letter combination that column in Excel notation
        Arguments:
            column_index (int): The integer to convert to Excel notation (0-indexed)
        Returns:
            (str): The letter representation of the index
        """
        return openpyxl.utils.get_column_letter(column_index+1)


def create_new_spreadsheet(client: gspread.Client, spreadsheet_name: str) -> SheetHandler:
    """
    Creates a new spreadsheet using the client, and wraps it in a SheetHandler
    Returns:
        (SheetHandler): The new spreadsheet as a SheetHandler
    """
    spreadsheet = client.create(spreadsheet_name)
    return SheetHandler(client, sheet_url = spreadsheet.url)

def copy_spreadsheet(client: gspread.Client, *, spreadsheet_url: str = "", spreadsheet_id: str = "", title: str = "") -> SheetHandler:
    """
    Copies a spreadsheet using the client, and wraps the copy in a SheetHandler
    Returns:
        (SheetHandler): The copy as a SheetHandler
    """
    if spreadsheet_url != "":
        sheet_connection = client.open_by_url(spreadsheet_url)
    elif spreadsheet_id != "":
        sheet_connection = client.open_by_key(spreadsheet_id)
    else:
        raise ValueError("Please supply either the sheet url or the sheet id")

    source = SheetHandler(client, sheet_url = spreadsheet_url, sheet_id = spreadsheet_id)
    if title == "":
        title = source.title
    copy = client.copy(source.id, title)
    return SheetHandler(client, sheet_url = copy.url)
