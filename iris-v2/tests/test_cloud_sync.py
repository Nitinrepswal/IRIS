from core.cloud_sync import CloudSync


def main():
    sync = CloudSync()

    print("Connected:", sync.is_connected())

    result = sync.upload({"name": "IRIS"})
    print("Upload before connection:")
    print(result)

    sync.connect()

    print("\nConnected:", sync.is_connected())

    result = sync.upload({"name": "IRIS"})
    print("Upload after connection:")
    print(result)

    result = sync.download()
    print("\nDownload:")
    print(result)

    sync.disconnect()

    print("\nConnected:", sync.is_connected())

    assert sync.is_connected() is False


if __name__ == "__main__":
    main()