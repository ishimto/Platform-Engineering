import subprocess

def run_cmd(cmd, input_text=None):
    res = subprocess.run(cmd, capture_output=True, text=True, check=False, input=input_text)
    return res.stdout or res.stderr, res.returncode

def create_namespace(ns):
    return run_cmd(["kubectl", "create", "namespace", ns])

def copy_secret(secret_name, src_ns, dst_ns):
    out, code = run_cmd(["kubectl", "get", "secret", secret_name, "-n", src_ns, "-o", "yaml"])
    if code != 0:
        return out, code
    patched = out.replace(f"namespace: {src_ns}", f"namespace: {dst_ns}")
    return run_cmd(["kubectl", "apply", "-n", dst_ns, "-f", "-"], input_text=patched)

def deploy_helm(release, namespace, image_tag, user):
    cmd = [
        "helm", "upgrade", "--install", release, "./charts/web_chart",
        "--namespace", namespace,
        "--set", f"deployment.tag={image_tag}",
        "--set", f"ingress.deployment.subdomain={user}",
        "--set", f"configmaps.mongodb.login=mongodb://root:changeme@mongodb.{namespace}.svc.cluster.local:27017"
    ]
    return run_cmd(cmd)


def deploy_mongodb(release, namespace):
    cmd = [
        "helm", "upgrade", "--install", f"{release}-mongodb", "./charts/mongodb",
        "--namespace", namespace
        ]
    return run_cmd(cmd)


def delete_namespace(namespace):
    return run_cmd(["kubectl", "delete", "namespace", namespace])


def get_status(namespace):
    return run_cmd(["kubectl", "get", "deployments,replicasets,pods,svc,ingresses", "-n", namespace, "-o", "wide"])
