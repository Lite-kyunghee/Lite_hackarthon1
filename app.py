# app.py
return jsonify({'msg': 'Assignment created', 'id': assignment.id}), 201


# ------------------------------
# 제출: 학생이 과제 제출
# ------------------------------
@app.route('/api/assignments/<int:assignment_id>/submit', methods=['POST'])
@jwt_required()
def submit_assignment(assignment_id):
    identity = get_jwt_identity()
    # 학생만 제출 가능(예제)
    if identity['role'] != 'student':
        return jsonify({'msg': 'Only students can submit'}), 403


if 'file' not in request.files:
    return jsonify({'msg': 'No file provided'}), 400


f = request.files['file']
filename = f"{int(datetime.utcnow().timestamp())}_{f.filename}"
save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
f.save(save_path)


submission = Submission(
assignment_id=assignment_id,
student_id=identity['id'],
file_path=filename,
submitted_at=datetime.utcnow()
)
db.session.add(submission)
db.session.commit()


return jsonify({'msg': 'Submitted', 'submission_id': submission.id}), 201


# ------------------------------
# 업로드된 파일 제공 (개발용)
# ------------------------------
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
# 로컬 업로드 폴더에서 파일을 전달. 운영시 접근 제어 추가 필요
return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ------------------------------
# 간단한 과제 조회(예제)
# ------------------------------
@app.route('/api/classes/<int:class_id>/assignments', methods=['GET'])
@jwt_required()
def list_assignments(class_id):
assignments = Assignment.query.filter_by(class_id=class_id).all()
# JSON으로 직렬화하여 반환 (간단 필드만 포함)
data = []
for a in assignments:
data.append({
'id': a.id,
'title': a.title,
'description': a.description,
'due_date': a.due_date.isoformat() if a.due_date else None,
'attachment_url': f"/uploads/{a.attachment}" if a.attachment else None
})
return jsonify(data)


# ------------------------------
# 실행부
# ------------------------------
if __name__ == '__main__':
# 개발용 실행 (디버그 모드)
app.run(host='0.0.0.0', port=5000, debug=True)