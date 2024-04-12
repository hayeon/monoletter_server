from flask import request, jsonify
# from fine_tuning.AI import callGpt


def receive_letter():
    data = request.json
    print(data)
    title = data.get('title')  
    letter = data.get('letter')

    #'title'과 'letter' 있는지 확인
    if not title or not letter:
        return jsonify({"error": "데이터가 충분하지 않습니다."}), 400

    else:
        print("문항:", title)
        print("내용:", letter)
    # feedback = callGpt(title, letter)
        feedback = "당신의 글은 개구립니다.🤮🤮"
        return jsonify(feedback)

