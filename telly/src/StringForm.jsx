import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

// Validation schema with Yup
const validationSchema = Yup.object().shape({
  data: Yup.string().min(5, 'Too short').required('Name required')
});

const handlePost = async (data) => {
  const config = {
    headers: {
      "Content-Type": "application/json"
    }
  };
  try {
    const response = await axios.post(
      `/api/arr_to_sorted_string/`,
      data,
      config
    );
    return response.data;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
};

const StringForm = () => {
  const postMutation = useMutation({
    mutationFn: (variables)=> handlePost(variables),
  });



  return (
    <div className="max-w-2xl border border-solid border-red-100 p-5 m-auto rounded-lg shadow-lg font-sans">
      <h1>API string to array</h1>
      <Formik
        initialValues={{ data: '' }}
        validationSchema={validationSchema}
        onSubmit={(values, { setSubmitting }) => {
          postMutation.mutate(values);
          setSubmitting(false);
        }}
      >
        {({ isSubmitting }) => (
          <Form className="flex flex-col gap-4">
            <div className="flex flex-col">
              <label htmlFor="data">Name:</label>
              <Field type="text" name="data" />
              <ErrorMessage name="data" component="div" className="text-red-500 text-base" />
            </div>

            <button 
            className={`
              text-white bg-emerald-600 hover:text-emerald-800 hover:bg-emerald-200 rounded-md p-4
              ${postMutation.isPending?"animate-bounce":"animate-none"}
              `} 
              type="submit" 
              disabled={isSubmitting||postMutation.isPending}>
              Send
            </button>
          </Form>
        )}
      </Formik>

      {postMutation.data && (
        <div className="mt-5 p-3 bg-white rounded-md">
          <h3>Validation Result:</h3>
          <pre>{JSON.stringify(postMutation.data, null, 2)}</pre>
        </div>
      )}

      {postMutation.isError && (
        <div className="text-red-500 text-base">
          <h3>Error:</h3>
          <p>{postMutation.error?.message || 'Unknown error'}</p>
        </div>
      )}
    </div>
  );
};

export default StringForm;
