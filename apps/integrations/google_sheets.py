"""
Google Sheets integration using gspread and gspread-formatting.
"""
import gspread
from gspread_formatting import (
    CellFormat, 
    TextFormat, 
    Color,
    format_cell_range,
    set_column_widths,
    set_row_height
)
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def get_gspread_client():
    """Get authenticated gspread client."""
    try:
        gc = gspread.service_account(filename=settings.GOOGLE_SERVICE_ACCOUNT_FILE)
        return gc
    except Exception as e:
        logger.error(f"Failed to authenticate with Google Sheets: {str(e)}")
        raise


def write_to_sheet(data, sheet_name, worksheet_name='Sheet1'):
    """
    Write data to a Google Sheet with custom formatting.
    
    Args:
        data: List of lists containing the data to write
        sheet_name: Name of the spreadsheet
        worksheet_name: Name of the worksheet (default: 'Sheet1')
    
    Returns:
        dict with status and sheet URL
    """
    try:
        # Get authenticated client
        gc = get_gspread_client()
        
        # Try to open existing spreadsheet or create new one
        try:
            spreadsheet = gc.open(sheet_name)
            logger.info(f"Opened existing spreadsheet: {sheet_name}")
        except gspread.SpreadsheetNotFound:
            spreadsheet = gc.create(sheet_name)
            logger.info(f"Created new spreadsheet: {sheet_name}")
        
        # Get or create worksheet
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
            # Clear existing content
            worksheet.clear()
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=len(data), cols=len(data[0]) if data else 10)
        
        # Write data to worksheet
        if data:
            worksheet.update(data, 'A1')
            logger.info(f"Wrote {len(data)} rows to worksheet")
            
            # Apply formatting
            apply_formatting(worksheet, len(data), len(data[0]))
        
        return {
            'status': 'success',
            'message': f'Data written to {sheet_name}/{worksheet_name}',
            'url': spreadsheet.url,
            'rows': len(data),
            'cols': len(data[0]) if data else 0
        }
        
    except Exception as e:
        logger.error(f"Error writing to Google Sheet: {str(e)}")
        raise


def apply_formatting(worksheet, num_rows, num_cols):
    """
    Apply custom formatting to the worksheet.
    - Header row: Bold, background color, center aligned
    - Data borders on all cells
    - Alternating row colors for readability
    """
    try:
        if num_rows == 0 or num_cols == 0:
            return
        
        # Format header row (row 1)
        header_format = CellFormat(
            backgroundColor=Color(0.2, 0.4, 0.6),  # Blue background
            textFormat=TextFormat(
                bold=True,
                foregroundColor=Color(1, 1, 1),  # White text
                fontSize=11
            ),
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE'
        )
        
        # Apply header formatting
        format_cell_range(worksheet, f'A1:{chr(64 + num_cols)}1', header_format)
        
        # Format data rows with alternating colors
        if num_rows > 1:
            # Even rows (light gray)
            even_row_format = CellFormat(
                backgroundColor=Color(0.95, 0.95, 0.95),
                textFormat=TextFormat(fontSize=10),
                verticalAlignment='MIDDLE'
            )
            
            # Odd rows (white)
            odd_row_format = CellFormat(
                backgroundColor=Color(1, 1, 1),
                textFormat=TextFormat(fontSize=10),
                verticalAlignment='MIDDLE'
            )
            
            # Apply alternating row colors
            for row in range(2, num_rows + 1):
                row_format = even_row_format if row % 2 == 0 else odd_row_format
                format_cell_range(worksheet, f'A{row}:{chr(64 + num_cols)}{row}', row_format)
        
        # Set column widths (auto-resize)
        set_column_widths(worksheet, [(chr(64 + i), 150) for i in range(1, num_cols + 1)])
        
        # Set header row height
        set_row_height(worksheet, '1', 30)
        
        logger.info(f"Applied formatting to {num_rows} rows and {num_cols} columns")
        
    except Exception as e:
        logger.error(f"Error applying formatting: {str(e)}")
        # Don't raise - formatting is nice to have but not critical


# Example usage function
def write_sample_data():
    """
    Example function to write sample data to a Google Sheet.
    """
    sample_data = [
        ['Name', 'Email', 'Department', 'Status'],
        ['John Doe', 'john@example.com', 'Engineering', 'Active'],
        ['Jane Smith', 'jane@example.com', 'Marketing', 'Active'],
        ['Bob Johnson', 'bob@example.com', 'Sales', 'Inactive'],
        ['Alice Williams', 'alice@example.com', 'Engineering', 'Active'],
    ]
    
    return write_to_sheet(sample_data, 'Webhook Service Test Sheet', 'Employee Data')

