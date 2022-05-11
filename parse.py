from argparse import ArgumentParser
from tempfile import NamedTemporaryFile
from pprint import pprint
import csv, os, pandas

"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

def is_row_skipped(row):
    for f in ['Cost Center', 'Budget Orgn']:
        if not isinstance(row[f], float)  and row[f].endswith('Total'):
            return True

    return False

if __name__ == "__main__":
    ap = ArgumentParser()

    ap.add_argument("filename")

    args = ap.parse_args()

    dim_cols = ['Cost Center', 'Budget Orgn', 'Budget Unit', 'Account', 'Account Title']
    amt_cols = ["2019-2020 Actual", "2020-2021 Actual",	"2021-2022 Budget", "2022-2023 Proposed"]
    all_cols = dim_cols + amt_cols

    xls = pandas.ExcelFile(args.filename)

    df = pandas.DataFrame(columns=all_cols)

    output = []
    for sheet_name in xls.sheet_names:
        fund_num, fund_name = sheet_name.split(',')[0].split(' - ', 1)

        sheet_df = pandas.read_excel(xls, sheet_name, skiprows=3)
        sheet_df['Fund'] = fund_num
        sheet_df['Fund Title'] = fund_name

        last_cost_center = None
        last_budget_orgn = None
        for row in sheet_df.to_dict('records')[:-1]:
            if is_row_skipped(row):
                continue
            if row['Cost Center'] is not None and not pandas.isna(row['Cost Center']):
                last_cost_center = row['Cost Center']
            if row['Budget Orgn'] is not None and not pandas.isna(row['Budget Orgn']):
                last_budget_orgn = row['Budget Orgn']
            if row['Cost Center'] is None or pandas.isna(row['Cost Center']):
                row['Cost Center'] = last_cost_center
            if row['Budget Orgn'] is None or pandas.isna(row['Budget Orgn']):
                row['Budget Orgn'] = last_budget_orgn

            #pprint(row)
            output.append(row)

    pandas.DataFrame(output).to_csv("Budget_2022_Parsed.csv", index=False)

