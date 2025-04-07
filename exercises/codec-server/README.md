# Exercise 2: Deploy a Codec Server and Integrate with the Web UI

During this exercise, you will:

* Review a Codec Server implementation
* Configure a Codec Server to share your custom converter logic
* Enable CORS and review other deployment parameters
* Integrate your Codec Server with the Temporal Web UI
* Securely return decoded results in the CLI and the Web UI

**Note: Part B of this Exercise does not work in the Codespaces Environment.**
If you want to demonstrate Codec Server Web UI integration, you'll need to clone this repository and run the exercise locally.

Make your changes to the code in the `practice` subdirectory (look for 
`TODO` comments that will guide you to where you should make changes to 
the code). If you need a hint or want to verify your changes, look at 
the complete version in the `solution` subdirectory.

### Activate the Virtual Environment
Ensure that the virtual environment you setup at the beginning of the
course is activated as detailed in the course [README](../../README.md#setup-your-python-virtual-environment).


## Part A: Configure a Codec Server to Use Your Data Converter

1. First, you'll review a barebones Codec Server implementation in Python, and
   make the necessary changes to integrate the Custom Data Converter from
   Exercise 1. Examine the `codec-server.py`. This file contains a complete HTTP
   server implementation using Python's
   [AIOHTTP](https://docs.aiohttp.org/en/stable/) library. It listens on
   endpoints at `/{namespace}/encode` and `/{namespace}/decode` as expected by
   the Temporal CLI, Web UI, and SDKs. This Codec Server needs one additional
   configuration detail before it can be deployed from sample code -- it needs
   to import the Codec logic from your own application, and then map the
   Converter logic on a per-Namespace basis. Add an `import` statement at the
   top of `codec-server.py` to import the `CompressionCodec` class from
   `codec.py`.
2. Next in `codec-server.py`, create a dictionary named `codecs` after initializing
   your `app` and before setting endpoints on it with `add_routes()` . Keys should
   be Namespace strings. Values should be Codec classes. By default, you only need
   to assign the `default` namespace to `CompressionCodec()` from this example.
3. After making these additions, you should have a functioning Codec Server,
   integrated with your application logic. Again, everything else in here is
   configured as generically as possible — note that this example Codec Server
   listens on port 8081, which is usually used in testing configurations — but
   this fulfills all the requirements of a Temporal Codec Server, and you could
   incorporate any other authentication requirements on top of HTTP as needed.
   Run your Codec Server from the root of your project directory with:
   
   ```shell
   python codec_server.py
   ```

   This will block the terminal it runs in, and await connections.
4. Now you can run your Custom Converter Workflow with the addition of data
   decoding. First, start the Worker:

   ```shell
   python worker.py
   ```

5. Next, from another terminal, run the Workflow starter:

   ```shell
   python starter.py
   ```

   The workflow should complete successfully without further modification.
6. Finally, run `temporal workflow show` for this exercise, with a
   `--codec-endpoint`:

   ```
   temporal workflow show \
      --workflow-id compression-workflow-id \
      --codec-endpoint 'http://localhost:8081/{namespace}'
   ```

   It should retain the same Event History as before, with the decoded result
   appended to the output:

   ```
   ...
   Result:
     Status: COMPLETED
     Output: ["Hello, Temporal"]
     ResultEncoding  json/plain
   ```

   You now have a working Codec Server implementation. In the following steps,
   you'll learn how to integrate it more closely with a Temporal Cluster for
   production environments.


## Part B: Enable CORS and Configure Temporal Web UI Integration

1. The next step is to enable Codec Server integration with the Temporal Web UI.
   This isn't necessary if you don't plan to use the Web UI to view your
   Workflow output, but it provides a stock example of how to integrate Codec
   Server requests into a web app, and is supported by Temporal Cloud. Without
   Codec Server integration, the Temporal Web UI cannot decode output, and
   results are displayed encoded:

   ![Encoded Workflow Output in Web UI](images/encoded-output.png)

   To do this, you first need to enable
   [CORS](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing), a common
   HTTP feature for securely making cross-domain requests.
   `codec-server.py` contains a function called `header_options()`
   which can add the necessary headers to your HTTP requests to support CORS,
   but it is not enabled by default. This example Codec Server exposes an
   additional command line parameter, `--web`, to conditionally enable CORS.
   Restart the Codec Server with the `--web` flag: `python codec_server.py --web
   http://localhost:8233`.
2. Now you can proceed to integrate your Codec Server with the Web UI. You
   should already have a local Temporal Cluster running that you can access in a
   browser at `http://localhost:8233` by default. In the top-right corner of the
   Web UI, you should see a 3D glasses icon, where you can access the Codec
   Server settings:

   ![Codec Server settings icon](images/configure-codec-server-button.png)

   In the Codec Server settings menu, add the path to your Codec Server, which
   should be `http://localhost:8081/default` by default. You do not need to toggle the
   user access token settings if you aren't using authentication.

   ![Codec Server settings](images/codec-server-settings.png)

   Note that you can toggle the "Use Cluster-level setting" option to save this
   Codec Server for all users of this cluster, or only for you, which would be
   especially relevant if you were running a `localhost` Codec Server with a
   remote Temporal Cluster. Click the "Apply" button. The 3D glasses in the
   top nav should now be colorized, indicating a successful connection:

   ![Codec Server enabled](images/codec-server-enabled.png)

3. When you navigate back to your Workflow History and scroll to the "Input
   and Results" section, you should find your payload automatically decoded by
   your Codec Server:

   ![Decoded Workflow Output in Web UI](images/decoded-output.png)

   You now have a working Codec Server integration with the Temporal Web UI.


### This is the end of the exercise.

