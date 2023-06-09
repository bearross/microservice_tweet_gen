import os
import pandas as pd
from datetime import datetime
from flask import request, jsonify, render_template

import pymysql
from api.semrush import get_semrush_metrics
from setting import app, mysql
from ownership.keywords_ownership import get_ownership_data, insert_pa_data

# for video transcript
# import urllib.request
# from extractor.headline_generator import generate_headline
# from segmentation.segment import segment_transcript
# from text_summarizer.summary import get_summary_from_text_spacy
# from video_transcription.transcript import transcript_video

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# # from extractor.keyword_extractor import get_keywords_from_bert
# from moviepy.editor import *


@app.route("/")
def home():
    return jsonify({"msg": "Welcome to TSOEV"})


@app.route('/key-own-upload-csv', methods=['POST'])
def set_keyword_url_csv():
    """ update database from csv file """
    account_id = request.form['account_id']

    csv_file = request.files.get('csv_file')
    final_filename = str(account_id) + "--" + datetime.now().strftime("%Y-%m-%d--%H:%M:%S") + ".csv"
    filepath = os.path.join(app.config['FILE_UPLOADS'], final_filename)
    csv_file.save(filepath)

    df = pd.read_csv(filepath)
    is_exist_pa = request.form['EnabledPA']
    if is_exist_pa:
        df_pa = df[['Keyword', 'URL', 'Position', 'Traffic', 'PA']].copy()
    else:
        input_df = df[['Keyword', 'URL', 'Position', 'Traffic']].copy()
        df_pa = insert_pa_data(input_df)

    ownership_df = get_ownership_data(df_pa)
    status = "failure"

    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for index, row in ownership_df.iterrows():
            _keyword, _url, _position, _traffic, _pa, _average_position, _average_traffic, _average_pa, _weighten_value, \
            _ownership_score, _date = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[
                9], formatted_date

            query = "INSERT INTO keyword_url_store VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (None, account_id, _keyword, _url, _position, _traffic, _pa, _average_position, _average_traffic, _average_pa,
                    _weighten_value,
                    _ownership_score, _date, None)
            cursor.execute(query, data)
            conn.commit()
            status = "ok"
            print(index)
    except Exception as e:
        status = "failure"
        print(e)
    finally:
        cursor.close()
        conn.close()

    response = jsonify({'op_status': status})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.route('/key-own-upload-raw', methods=['POST'])
def set_keyword_url_data():
    """ update database from user-driven data """
    account_id = request.form['account_id']

    if request.form['PA'] is None:
        df = pd.DataFrame({'Keyword': [request.form['Keyword']], 'URL': [request.form['URL']],
                           'Position': [int(request.form['Position'])],
                           'Traffic': [int(request.form['Traffic'])]})
        df_pa = insert_pa_data(df)
    else:
        df_pa = pd.DataFrame({'Keyword': [request.form['Keyword']], 'URL': [request.form['URL']],
                              'Position': [int(request.form['Position'])],
                              'Traffic': [int(request.form['Traffic'])], 'PA': [int(request.form['PA'])]})

    ownership_df = get_ownership_data(df_pa)
    status = "failure"

    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for index, row in ownership_df.iterrows():
            _keyword, _url, _position, _traffic, _pa, _average_position, _average_traffic, _average_pa, _weighten_value, \
            _ownership_score, _date = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[
                9], formatted_date

            query = "INSERT INTO keyword_url_store VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (None, account_id, _keyword, _url, _position, _traffic, _pa, _average_position, _average_traffic, _average_pa,
                    _weighten_value,
                    _ownership_score, _date, None)

            cursor.execute(query, data)
            conn.commit()
            status = "ok"
    except Exception as e:
        status = "failure"
        print(e)
    finally:
        cursor.close()
        conn.close()

    response = jsonify({'op_status': status})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.route('/key-own-from-url', methods=['POST'])
def set_keyword_url_txt():
    """ update database from semrush output """
    url = request.form['Url']
    account_id = request.form['account_id']

    semrush_output = get_semrush_metrics(url)
    df = pd.DataFrame(semrush_output)

    input_df = df[['Keyword', 'Url', 'Position', 'Traffic']].copy()
    df_pa = insert_pa_data(input_df)
    ownership_df = get_ownership_data(df_pa)
    status = "failure"

    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for index, row in ownership_df.iterrows():
            _keyword, _url, _position, _traffic, _pa, _average_position, _average_traffic, _average_pa, _weighten_value, \
            _ownership_score, _date = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[
                9], formatted_date

            query = "INSERT INTO keyword_url_store VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (None, account_id, _keyword, _url, _position, _traffic, _pa, _average_position, _average_traffic, _average_pa,
                    _weighten_value,
                    _ownership_score, _date, None)

            cursor.execute(query, data)
            conn.commit()
            status = "ok"
    except Exception as e:
        status = "failure"
        print(e)
    finally:
        cursor.close()
        conn.close()

    response = jsonify({'op_status': status})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.route('/own-keyword', methods=['POST'])
def set_url_to_keyword():
    """ Only one URL owns each given keyword """
    account_id = request.form['account_id']
    status = "failure"
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "set SQL_SAFE_UPDATES = 0"
        cursor.execute(query)
        conn.commit()
        query = "DELETE FROM keyword_url_store WHERE Id NOT IN (SELECT * FROM (SELECT MAX(Id) FROM keyword_url_store WHERE account_id='{}' GROUP BY Url) as t)".format(account_id)
        cursor.execute(query)
        conn.commit()
        query = "set SQL_SAFE_UPDATES = 1"
        cursor.execute(query)
        conn.commit()
        status = "ok"
    except Exception as e:
        status = "failure"
        print(e)
    finally:
        cursor.close()
        conn.close()

    response = jsonify({'op_status': status})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.route('/key-own-refresh', methods=['POST'])
def update_keyword_ownership():
    """ refresh the data to recalculate keyword ownership """
    account_id = request.form['account_id']
    status = "failure"
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM keyword_url_store WHERE update_date in (SELECT MAX(update_date) FROM keyword_url_store WHERE account_id='{}' GROUP BY keyword)".format(account_id)
        cursor.execute(query)
        saved_output = cursor.fetchall()
        df = pd.DataFrame(saved_output)
        drop_df = df.drop(columns=['Id', 'account_id'])

        ownership_df = get_ownership_data(drop_df)
        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for index, row in ownership_df.iterrows():
            _keyword, _url, _position, _traffic, _pa, _average_position, _average_traffic, _average_pa, _weighten_value, \
            _ownership_score, _date = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[
                9], formatted_date
            query = "INSERT INTO keyword_url_store VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (None, account_id, _keyword, _url, _position, _traffic, _pa, _average_position, _average_traffic, _average_pa,
                    _weighten_value, _ownership_score, _date, None)

            cursor.execute(query, data)
            conn.commit()
            status = "ok"
    except Exception as e:
        status = "failure"
        print(e)
    finally:
        cursor.close()
        conn.close()

    response = jsonify({'op_status': status})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.route('/key-own-revert', methods=['POST'])
def revert_keyword_ownership():
    """ revert to previous versions of the keyword to URL mappings """
    account_id = request.form['account_id']
    status = "failure"
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "set SQL_SAFE_UPDATES = 0"
        cursor.execute(query)
        conn.commit()
        query = "DELETE FROM keyword_url_store WHERE update_date in (SELECT * FROM (SELECT MAX(update_date) FROM keyword_url_store WHERE account_id='{}' GROUP BY keyword) as t)".format(account_id)
        cursor.execute(query)
        conn.commit()
        query = "set SQL_SAFE_UPDATES = 1"
        cursor.execute(query)
        conn.commit()
        status = "ok"
    except Exception as e:
        status = "failure"
        print(e)
    finally:
        cursor.close()
        conn.close()

    response = jsonify({'op_status': status})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.route('/key-own-get-db', methods=['POST'])
def get_all_keyword_ownership():
    """ get all data in mysql database """
    account_id = request.form['account_id']
    status = "failure"
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM keyword_url_store WHERE update_date in (SELECT MAX(update_date) FROM keyword_url_store WHERE account_id='{}' GROUP BY keyword)".format(account_id)
        cursor.execute(query)
        saved_output = cursor.fetchall()
        df = pd.DataFrame(saved_output)

        if not df.empty:
            drop_df = df.drop(columns=['Id'])
            ownership_df = get_ownership_data(drop_df)
        else:
            ownership_df = pd.DataFrame({})
        status = "ok"
    except Exception as e:
        status = "failure"
        ownership_df = pd.DataFrame({})
        print(e)
    finally:
        cursor.close()
        conn.close()

    ownership_dict = ownership_df.to_dict(orient='dict')
    ownership_dict.update({'op_status': status})

    response = jsonify(ownership_dict)
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.route('/key-own-reset-db', methods=['POST'])
def delete_all_keyword_ownership():
    """ delete all data in mysql database """
    account_id = request.form['account_id']
    status = "failure"
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "set SQL_SAFE_UPDATES = 0"
        cursor.execute(query)
        conn.commit()
        query = "DELETE FROM keyword_url_store WHERE account_id='{}'".format(account_id)
        cursor.execute(query)
        conn.commit()
        query = "set SQL_SAFE_UPDATES = 1"
        cursor.execute(query)
        conn.commit()
        status = "ok"
    except Exception as e:
        status = "failure"
        print(e)
    finally:
        cursor.close()
        conn.close()

    response = jsonify({'op_status': status})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


# @app.route('/transcript-from-file', methods=['POST'])
# def transcript_video_file():
#     """ transcript video by uploaded video and create HTML indicate the topic """
#
#     uploaded_file = request.files.get('video_file')
#     save_path = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
#     uploaded_file.save(save_path)
#
#     text = transcript_video(save_path)
#     abstract = get_summary_from_text_spacy(text)
#     contents = segment_transcript(text)
#
#     keywords = []
#     for passage in contents:
#       content_headline = generate_headline(["summarize: " + passage])
#       keywords.append(content_headline[0])
#
#     return render_template('transcript.html', headerline=headlines[0], summary=abstract, topic_list=keywords, content_list=contents, size=len(keywords))


# @app.route('/transcript-from-url', methods=['POST'])
# def transcript_video_url():
#     """ transcript video by url and create HTML indicate the topic """
#     video_url = request.form['video_url']
#     filename = formatted_date = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
#     save_path = os.path.join(app.config['FILE_UPLOADS'], filename + ".ts")
#     urllib.request.urlretrieve(video_url, save_path)
#
#     text = transcript_video(save_path)
#     abstract = get_summary_from_text_spacy(text)
#     headlines = generate_headline(["summarize: " + abstract])
#     contents = segment_transcript(text)
#
#     keywords = []
#     for passage in contents:
#         content_headline = generate_headline(["summarize: " + passage])
#         keywords.append(content_headline[0])
#
#     return render_template('transcript.html', headerline=headlines[0], summary=abstract, topic_list=keywords,
#                            content_list=contents, size=len(keywords))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006)
