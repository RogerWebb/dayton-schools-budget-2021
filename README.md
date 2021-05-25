Dayton Budget Data Preprocessor.  This tool breaks the Account and Budget Organization columns into separate fields (leaving the original in place), maps the Cost Center to Cost Center Name which includes human-readable values for this column as well as breaking the 4 budget year Amount columns into a single Amount column with the years being represented in the Budget Term column.  This is the data set used to drive the dashboard linked below with the exception that the dashboard computed the Cost Center Name field in Data Studio where I've modified this script to compute it in advance for future use.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Installation
------------

Requires Git, Python 3.7+

git clone git@github.com:RogerWebb/dayton-schools-budget-2021.git src
cd src
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

Use
---

python prep.py ./SPREADSHEET\ FOR\ BUDGET\ COMMITTEE\ 5.12.2021.xlsx --output Dayton_Budget_2021_Preprocessed.csv

