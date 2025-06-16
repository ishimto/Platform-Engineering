from flask import Flask, request, render_template
from modules.actions import *
from modules.mongo import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/create', methods=['GET', 'POST'])
def deploy():
    if request.method == 'GET':
        return render_template('deploy_form.html')

    user = request.form['username'].strip().lower()
    tag = request.form['image_tag'].strip()
    ns = f"dev-{user}"
    release = f"dev-{user}-app"
    logs = []

    out, _ = create_namespace(ns)
    logs.append(out)

    secret_out, code = copy_secret("vault-dev-token", "default", ns)
    logs.append(secret_out)

    helm_out, helm_code = deploy_helm(release, ns, tag, user)
    logs.append(helm_out)
    
    helm_out, mongo_code = deploy_mongodb(release, ns)
    logs.append(helm_out)


    return render_template('result.html', logs="\n".join(logs), success=(mongo_code == 0 and helm_code == 0))


@app.route('/delete', methods=['GET', 'POST'])
def delete_route():
    if request.method != 'POST':
        return render_template('delete_form.html')
    user = request.form['username'].strip().lower()
    ns = f"dev-{user}"
    out, code = delete_namespace(ns)
    return render_template('result.html', logs=out, success=(code == 0))


@app.route('/status', methods=['GET', 'POST'])
def status():
    if request.method == 'GET':
        return render_template('status_form.html')

    user = request.form['username'].strip().lower()
    ns = f"dev-{user}"
    out, code = get_status(ns)
    if "No resources found" in out:
        code = 1
    return render_template('result.html', logs=out, success=(code == 0))


@app.route('/stats', methods=['GET', 'POST'])
def stats():
    if request.method == 'GET':
        return render_template('stats.html')
    
    user = request.form['username'].strip().lower()
    ns = f"dev-{user}"
    release = f"dev-{user}-app"
    counts = get_city_counts(release, ns)

    return render_template("city_counts.html", counts=counts, namespace=ns, release=release)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
