import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

// Validation schema with Yup
const validationSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email address').required('Email is required'),
  url: Yup.string().url('Invalid URL').required('API URL is required'),
});

const handleValidation = async (data) => {
  const config = {
    headers: {
      "Content-Type": "application/json"
    }
  };
  try {
    const response = await axios.post(
      `/api/validation/`,
      data,
      config
    );
    return response.data;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
};

const AppForm = () => {
  const validationMutation = useMutation({
    mutationFn: (variables)=> handleValidation(variables),
  });



  return (
    <div className="max-w-2xl border border-solid border-red-100 p-5 m-auto rounded-lg shadow-lg font-sans">
      <h1>API Validator</h1>
      <Formik
        initialValues={{ email: '', url: '' }}
        validationSchema={validationSchema}
        onSubmit={(values, { setSubmitting }) => {
          validationMutation.mutate(values);
          setSubmitting(false);
        }}
      >
        {({ isSubmitting }) => (
          <Form className="flex flex-col gap-4">
            <div className="flex flex-col">
              <label htmlFor="email">Email:</label>
              <Field type="email" name="email" />
              <ErrorMessage name="email" component="div" className="text-red-500 text-base" />
            </div>

            <div className="flex flex-col">
              <label htmlFor="url">API URL:</label>
              <Field type="url" name="url" />
              <ErrorMessage name="url" component="div" className="text-red-500 text-base" />
            </div>

            <button className={`
              text-white bg-purple-700 hover:text-purple-800 hover:bg-purple-200 rounded-md p-4
              ${validationMutation.isPending?"animate-bounce":"animate-none"}
              `} 
              type="submit" 
              disabled={isSubmitting||validationMutation.isPending}>
              Validate
            </button>
          </Form>
        )}
      </Formik>

      {validationMutation.data && (
        <div className="mt-5 p-3 bg-white rounded-md">
          <h3>Validation Result:</h3>
          <pre>{JSON.stringify(validationMutation.data, null, 2)}</pre>
        </div>
      )}

      {validationMutation.isError && (
        <div className="text-red-500 text-base">
          <h3>Error:</h3>
          <p>{validationMutation.error?.message || 'Unknown error'}</p>
        </div>
      )}
    </div>
  );
};

export default AppForm;
