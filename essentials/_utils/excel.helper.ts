// https://github.com/exceljs/exceljs
import * as Excel from 'exceljs';

export const buildWorkbook = (): Excel.Workbook => {
    return new Excel.Workbook();
}

export const buildWorksheet = (workbook: Excel.Workbook, name: string): Excel.Worksheet => {
    return workbook.addWorksheet(name);
}

/**
 * Generate Columns of worksheet
 * @param worksheet Sheet to work in
 * @param columns Columns like [{header: 'Id', key: 'id', width: 10},{header: 'Name', key: 'name', width: 32 }]
 */
export const buildColumns = (worksheet: Excel.Worksheet, columns: { header: string; key: string; width: number; }[]): Excel.Worksheet => {
    worksheet.columns = columns;
    return worksheet
} 

/**
 * Add a row by contiguous Array (assign to columns A, B, C ...)
 * @param worksheet heet to work in
 * @param contiguousValues [A, B, C ...] values
 * @returns heet to work in with row added
 */
export const buildContiguousRow = (worksheet: Excel.Worksheet, contiguousValues: [string, string, string | number]): Excel.Worksheet => {
    worksheet.addRow(contiguousValues);
    return worksheet
}

export const writeExcel = async (workbook: Excel.Workbook, fileNamePath: string) => {
    await workbook.xlsx.writeFile(fileNamePath);
}