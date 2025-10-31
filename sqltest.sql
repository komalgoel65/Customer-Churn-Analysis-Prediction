CREATE TABLE LargeDataTable (
    RecordID BIGINT PRIMARY KEY IDENTITY(1,1), -- Use BIGINT for large ID ranges
    DataField1 VARCHAR(MAX), -- Use MAX for potentially large text data
    DataField2 NVARCHAR(MAX), -- Use NVARCHAR(MAX) for large Unicode text data
    NumericValue DECIMAL(18, 4), -- Use appropriate precision for numeric data
    DateTimeStamp DATETIME2, -- Use DATETIME2 for precise timestamping
    BlobData VARBINARY(MAX), -- Use VARBINARY(MAX) for large binary data (e.g., images, files)
    Category INT,
    StatusFlag BIT,
    -- Add more columns as needed, choosing data types suitable for anticipated data size
    INDEX IX_DateTimeStamp (DateTimeStamp), -- Index for common queries on date/time
    INDEX IX_Category (Category) -- Index for filtering or grouping by category
);