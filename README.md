# invisible-python

Python source code, minus the source code you can see.

**In:**

```python
print("Hello World!")
```

**Out:**

<pre> 			     			  	  		 	  	 		 			  			 	    	 	     	   	  	  	    		  	 	 		 		   		 		   		 				  	      	 	 			 		 				 			  	  		 		   		  	    	    	  	   	   	 	  	</pre>

That's the actual output. Your code is still there. It just has nothing to say.

Each byte becomes eight bits: space for `0`, tab for `1`, most significant bit first.
Only spaces and tabs. No newlines. Eight times the file size. Negative compression.

Python 3.10+, no runtime dependencies.

```sh
pip install -e .
echo 'print("Hello World!")' > hello.py
ipy encode hello.py
ipy run hello.ipy
ipy cat hello.ipy
ipy cat hello.ipy > restored.py
```

Use `-o other.ipy` with `encode`, or pass script arguments after `run hello.ipy`.
`python3 -m invisible_python` also works.

Encode `secret_module.py`, remove or rename the original, then:

```python
import invisible_python
invisible_python.install()
import secret_module
```

Packages use `__init__.ipy`; relative imports work. Normal Python imports take
priority. `ipy run` enables invisible imports from the script's directory automatically.

**Obfuscation, not encryption or security.** The bugs are invisible too.
Only run code you trust.

Tests:

```sh
pip install -e '.[test]'
pytest
```
