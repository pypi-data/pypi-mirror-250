use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyclass]
struct Foo {
    name: String,
}

#[pymethods]
impl Foo {
    fn __str__(slf: PyRef<'_, Self>) -> String {
       slf.to_string() 
    }
}

impl std::fmt::Display for Foo {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Name: {}", self.name)
    }
}

#[pyfunction]
fn summer(py: Python<'_>, foo: String) -> PyResult<&PyAny>{
    pyo3_asyncio::tokio::future_into_py(py, async move {
        println!("foo: {foo}");
        let f = Foo {name: foo};
        // println!("{py:?}");
        Ok(Python::with_gil(|py| f))
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn jansson_string_sum(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(summer, m)?)?;
    Ok(())
}

