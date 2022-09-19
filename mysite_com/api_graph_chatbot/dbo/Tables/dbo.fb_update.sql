CREATE TABLE [dbo].[fb_update](
	[guid] [varchar](max) NULL,
	[post_id] [varchar](max) NULL,
	[id] [varchar](max) NULL,
	[message] [varchar](max) NULL,
	[status_code] [float] NULL,
	[post_url] [varchar](max) NULL,
	[JSON] [varchar](max) NULL,
	[response_time] [float] NULL,
	[execution_time] [float] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO