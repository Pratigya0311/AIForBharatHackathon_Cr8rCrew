"""
AWS CDK Stack for TrendScribe - Simplified for CDK 2.x
Creates DynamoDB tables and S3 bucket for TrendScribe application.
"""

import os
from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    Duration,
    RemovalPolicy,
    Stack,
    Tags,
    CfnOutput
)
from constructs import Construct


class TrendScribeStack(Stack):
    """CDK Stack for TrendScribe - creates core AWS resources."""

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        env_name = os.getenv('ENVIRONMENT', 'dev')
        self._create_dynamodb_tables(env_name)
        self._create_s3_bucket(env_name)

    def _create_dynamodb_tables(self, env_name):
        """Create 3 DynamoDB tables: CreatorProfiles, Scripts, Trends."""
        
        # CreatorProfiles Table - stores creator style information
        creator_profiles_table = dynamodb.Table(
            self, "CreatorProfiles",
            partition_key=dynamodb.Attribute(
                name="userId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )
        Tags.of(creator_profiles_table).add("Name", "CreatorProfiles")
        Tags.of(creator_profiles_table).add("Environment", env_name)
        
        # Scripts Table - stores generated scripts
        scripts_table = dynamodb.Table(
            self, "Scripts",
            partition_key=dynamodb.Attribute(
                name="userId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="scriptId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )
        Tags.of(scripts_table).add("Name", "Scripts")
        Tags.of(scripts_table).add("Environment", env_name)
        
        # Trends Table - stores analyzed trends with TTL
        trends_table = dynamodb.Table(
            self, "Trends",
            partition_key=dynamodb.Attribute(
                name="userId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="trendId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
            time_to_live_attribute="ttl",  # 48-hour auto-expiration
        )
        Tags.of(trends_table).add("Name", "Trends")
        Tags.of(trends_table).add("Environment", env_name)
        
        # Store references for later use
        self.creator_profiles_table = creator_profiles_table
        self.scripts_table = scripts_table
        self.trends_table = trends_table

    def _create_s3_bucket(self, env_name):
        """Create S3 bucket for content and scripts storage."""
        
        s3_bucket = s3.Bucket(
            self, "TrendScribeData",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )
        
        Tags.of(s3_bucket).add("Name", "TrendScribeData")
        Tags.of(s3_bucket).add("Environment", env_name)
        
        self.s3_bucket = s3_bucket
        
        # Output resource names
        CfnOutput(
            self, "BucketName",
            value=self.s3_bucket.bucket_name,
            description="S3 Bucket Name for content and scripts"
        )
        
        CfnOutput(
            self, "CreatorProfilesTableName",
            value=self.creator_profiles_table.table_name,
            description="DynamoDB CreatorProfiles Table Name"
        )
        
        CfnOutput(
            self, "ScriptsTableName",
            value=self.scripts_table.table_name,
            description="DynamoDB Scripts Table Name"
        )
        
        CfnOutput(
            self, "TrendsTableName",
            value=self.trends_table.table_name,
            description="DynamoDB Trends Table Name"
        )
