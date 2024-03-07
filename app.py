from flask import Flask, render_template, request , jsonify
import NoLimit # Assuming my_function.py contains the function you want to run

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        # Call your function from my_function.py
        result_value = NoLimit.StartCalculation()
        return render_template('result.html', result=result_value)

@app.route('/calculate', methods=['POST'])
def aditya():
    mfIndex = int(request.form['value'])
    print("MF Index: "+str(mfIndex))
    result_value = NoLimit.individualCalc(mfIndex)
    return jsonify(output=result_value)

if __name__ == '__main__':
    app.run(debug=True)
