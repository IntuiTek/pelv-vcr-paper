import sys, yaml, json

def validate(md):
    errors = []
    if len(md.get('abstract','')) > 1920:
        errors.append("Abstract exceeds 1920 chars")
    if len(md.get('comments','')) > 192:
        errors.append("Comments exceed 192 chars")
    for fld in ('title','authors','abstract','categories'):
        if fld not in md:
            errors.append(f"Missing required field: {fld}")
    if errors:
        raise ValueError("Metadata errors:\n" + "\n".join(errors))

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    md = yaml.safe_load(open(src))
    validate(md)
    with open(dst, 'w') as f:
        json.dump(md, f, indent=2) 