import streamlit as st

import yaml

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


st.write("# Autograder")


ans_arr = []
model = SentenceTransformer('bert-base-nli-mean-tokens')


def stinit():
    with st.form("autograder_form", clear_on_submit=True):
        st.write("### Question:")
        ques = st.text_area(label="Question",
                            placeholder="please type the question here")

        st.write("### Reference answer:")
        ref_answer = st.text_area(label="Reference answer",
                                  placeholder="please type the reference answer here")

        ans_arr.append(ref_answer)

        st.write("### Student answer:")
        stu_answer = st.text_area(label="Student answer",
                                  placeholder="please enter the student answer here")

        ans_arr.append(stu_answer)

        option = st.selectbox(
            'Choose Grading type:',
            ('out of grade(number) ex:(/100)', 'percentage score (%)'))

        num = st.number_input('please enter the maximum marks:')

        submit = st.form_submit_button("Submit")

    if submit:
        ans_embed = model.encode(ans_arr)
        result = cosine_similarity([ans_embed[0]], ans_embed[1:])
        if option == 'percentage score (%)':
            st.write("The Score is: ", round(
                ((result[0][0]*num)/num)*100, 2), "%")
            # st.write("The similarity score is: ", round(result[0][0], 1))
        elif option == 'out of grade(number) ex:(/100)':
            st.write("The Score is: ", round(result[0][0]*num, 2))
            # st.write("The similarity score is: ", round(result[0][0], 1))


# hashed_passwords = stauth.Hasher(['admin', 'lorem']).generate()
# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=yaml.SafeLoader)

# option = st.sidebar.selectbox(
#     'Login/SignUp',
#     ('Login', 'SignUp'))

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized'])

# if option == "Login":

#     name, authentication_status, username = authenticator.login(
#         'Login', 'main')
#     if st.session_state["authentication_status"]:
#         authenticator.logout('Logout', 'main')

#         stinit()
#     elif st.session_state["authentication_status"] == False:
#         st.error('Username/password is incorrect')
#     elif st.session_state["authentication_status"] == None:
#         st.warning('Please enter your username and password')

# if option == "SignUp":
#     try:
#         if authenticator.register_user('Register user', preauthorization=True):
#             st.success('User registered successfully, you can login now')

#             with open('config.yaml', 'w') as file:
#                 yaml.dump(config, file, default_flow_style=False)
#     except Exception as e:
#         st.error(e)
