# Roblox Account Launcher

This Python package provides a simple interface for launching Roblox games using an authenticated account. It includes functions to obtain necessary authentication tokens and launch a specified Roblox game.

## Prerequisites

Before using this package, ensure that you have the following installed:

- Python 3.x
- Required Python packages: `os`, `subprocess`, `platform`, `requests`, `random`

## Usage

1. Import the `AccountLaunch` class from the package.

   ```python
   from your_package_name import AccountLaunch
   ```

2. Initialize an `AccountLaunch` object with the Roblox account's cookie and the target place ID.

   ```python
   account_launcher = AccountLaunch(cookie="your_cookie_here", placeId="target_place_id")
   ```

3. Obtain the required authentication tokens.

   ```python
   xsrf_token = account_launcher.get_xsrf()
   authentication_ticket = account_launcher.get_authentication_ticket()
   ```

4. Retrieve the Job ID for the target game.

   ```python
   job_id = account_launcher.job_id()
   ```

5. Launch Roblox with the specified parameters.

   ```python
   launch_result = account_launcher.launch_roblox(ticket=authentication_ticket, job_id=job_id)
   print(launch_result)
   ```

## Notes

- The package assumes that Roblox is installed in the default directory on Windows. If not, it attempts to find the installation path in the local AppData directory.
- Ensure that the required packages are installed using `pip install os subprocess platform requests random`.

## Example

```python
from your_package_name import AccountLaunch

# Initialize AccountLaunch object
account_launcher = AccountLaunch(cookie="your_cookie_here", placeId="target_place_id")

# Get authentication tokens
xsrf_token = account_launcher.get_xsrf()
authentication_ticket = account_launcher.get_authentication_ticket()

# Get the Job ID
job_id = account_launcher.job_id()

# Launch Roblox
launch_result = account_launcher.launch_roblox(ticket=authentication_ticket, job_id=job_id)
print(launch_result)
```

## License

This package is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.