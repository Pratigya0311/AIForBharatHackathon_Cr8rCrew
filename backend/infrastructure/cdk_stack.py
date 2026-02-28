"""
AWS CDK Stack for TrendScribe
Defines all AWS resources: DynamoDB, S3, Lambda, API Gateway, Cognito, IAM.
"""

import os
from aws_cdk import (
    core,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_cognito as cognito,
    aws_iam as iam,
    aws_logs as logs,
    Duration,
    RemovalPolicy,
    Expiration
)


class TrendScribeStack(core.Stack):
    """
    CDK Stack for TrendScribe AWS infrastructure.
    
    Resources:
    - 3 DynamoDB tables (CreatorProfiles, Scripts, Trends)
    - 1 S3 bucket for content and scripts
    - 3 Lambda functions (one per Phase 2 handler)
    - 1 API Gateway REST API
    - 1 Cognito User Pool for authentication
    - IAM roles with least privilege
    - CloudWatch log groups
    """

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Environment configuration
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.env_name = os.getenv('ENVIRONMENT', 'dev')
        
        # Create resources
        self._create_dynamodb_tables()
        self._create_s3_bucket()
        self._create_iam_roles()
        self._create_lambda_functions()
        self._create_api_gateway()
        self._create_cognito_pool()
        self._create_cloudwatch_logs()
        
        # Output resource information
        self._output_resource_info()

    # ========================================================================
    # DYNAMODB TABLES
    # ========================================================================

    def _create_dynamodb_tables(self):
        """Create 3 DynamoDB tables with proper configuration."""
        
        # CreatorProfiles Table
        self.creator_profiles_table = dynamodb.Table(
            self, "CreatorProfiles",
            partition_key=dynamodb.Attribute(
                name="userId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # For demo only
            point_in_time_recovery=True,
            stream=dynamodb.StreamSpecification.NEW_AND_OLD_IMAGES
        )
        
        core.Tags.of(self.creator_profiles_table).add("Name", "CreatorProfiles")
        core.Tags.of(self.creator_profiles_table).add("Environment", self.env_name)
        
        # Scripts Table
        self.scripts_table = dynamodb.Table(
            self, "Scripts",
            partition_key=dynamodb.Attribute(
                name="scriptId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="userId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # For demo only
            point_in_time_recovery=True,
            stream=dynamodb.StreamSpecification.NEW_AND_OLD_IMAGES
        )
        
        # Add GSI for querying by userId
        self.scripts_table.add_global_secondary_index(
            index_name="userId-createdAt-index",
            partition_key=dynamodb.Attribute(
                name="userId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="createdAt",
                type=dynamodb.AttributeType.STRING
            ),
            projection=dynamodb.ProjectionType.ALL
        )
        
        core.Tags.of(self.scripts_table).add("Name", "Scripts")
        core.Tags.of(self.scripts_table).add("Environment", self.env_name)
        
        # Trends Table with TTL
        self.trends_table = dynamodb.Table(
            self, "Trends",
            partition_key=dynamodb.Attribute(
                name="trendId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # For demo only
            point_in_time_recovery=True,
            time_to_live_attribute="ttl",  # 48-hour auto-expiration
            stream=dynamodb.StreamSpecification.NEW_AND_OLD_IMAGES
        )
        
        core.Tags.of(self.trends_table).add("Name", "Trends")
        core.Tags.of(self.trends_table).add("Environment", self.env_name)

    # ========================================================================
    # S3 BUCKET
    # ========================================================================

    def _create_s3_bucket(self):
        """Create S3 bucket with versioning and encryption."""
        
        self.s3_bucket = s3.Bucket(
            self, "TrendScribeData",
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,  # For demo only
            auto_delete_objects=True,
            lifecycle_rules=[
                s3.LifecycleRule(
                    expiration=Duration.days(90),
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                            transition_after=Duration.days(30)
                        )
                    ]
                )
            ]
        )
        
        core.Tags.of(self.s3_bucket).add("Name", "TrendScribeData")
        core.Tags.of(self.s3_bucket).add("Environment", self.env_name)

    # ========================================================================
    # IAM ROLES
    # ========================================================================

    def _create_iam_roles(self):
        """Create IAM roles with least privilege for Lambda functions."""
        
        # Content Processor Lambda Role
        self.content_processor_role = iam.Role(
            self, "ContentProcessorRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Role for Content Processor Lambda"
        )
        
        # Permissions: Bedrock + DynamoDB (CreatorProfiles) + S3
        self.content_processor_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaBasicExecutionRole")
        )
        self.content_processor_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel"
                ],
                resources=["*"]
            )
        )
        self.creator_profiles_table.grant_write_data(self.content_processor_role)
        self.s3_bucket.grant_read_write(self.content_processor_role)
        
        # Trend Analyzer Lambda Role
        self.trend_analyzer_role = iam.Role(
            self, "TrendAnalyzerRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Role for Trend Analyzer Lambda"
        )
        
        self.trend_analyzer_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaBasicExecutionRole")
        )
        self.trend_analyzer_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel"
                ],
                resources=["*"]
            )
        )
        self.trends_table.grant_read_data(self.trend_analyzer_role)
        self.creator_profiles_table.grant_read_data(self.trend_analyzer_role)
        
        # Script Generator Lambda Role
        self.script_generator_role = iam.Role(
            self, "ScriptGeneratorRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Role for Script Generator Lambda"
        )
        
        self.script_generator_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaBasicExecutionRole")
        )
        self.script_generator_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel"
                ],
                resources=["*"]
            )
        )
        self.scripts_table.grant_write_data(self.script_generator_role)
        self.trends_table.grant_read_data(self.script_generator_role)
        self.s3_bucket.grant_read_write(self.script_generator_role)

    # ========================================================================
    # LAMBDA FUNCTIONS
    # ========================================================================

    def _create_lambda_functions(self):
        """Create 3 Lambda functions for Phase 2 handlers."""
        
        # Content Processor Lambda
        self.content_processor_lambda = lambda_.Function(
            self, "ContentProcessor",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("backend/lambdas/handlers"),
            handler="content_processor.lambda_handler",
            role=self.content_processor_role,
            timeout=Duration.seconds(60),
            memory_size=512,
            environment={
                "AWS_REGION": self.region,
                "CREATOR_PROFILES_TABLE": self.creator_profiles_table.table_name,
                "S3_BUCKET_NAME": self.s3_bucket.bucket_name
            }
        )
        
        # Trend Analyzer Lambda
        self.trend_analyzer_lambda = lambda_.Function(
            self, "TrendAnalyzer",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("backend/lambdas/handlers"),
            handler="trend_analyzer.lambda_handler",
            role=self.trend_analyzer_role,
            timeout=Duration.seconds(60),
            memory_size=512,
            environment={
                "AWS_REGION": self.region,
                "TRENDS_TABLE": self.trends_table.table_name,
                "CREATOR_PROFILES_TABLE": self.creator_profiles_table.table_name
            }
        )
        
        # Script Generator Lambda
        self.script_generator_lambda = lambda_.Function(
            self, "ScriptGenerator",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("backend/lambdas/handlers"),
            handler="script_generator_handler.lambda_handler",
            role=self.script_generator_role,
            timeout=Duration.seconds(120),
            memory_size=1024,
            environment={
                "AWS_REGION": self.region,
                "SCRIPTS_TABLE": self.scripts_table.table_name,
                "TRENDS_TABLE": self.trends_table.table_name,
                "S3_BUCKET_NAME": self.s3_bucket.bucket_name
            }
        )

    # ========================================================================
    # API GATEWAY
    # ========================================================================

    def _create_api_gateway(self):
        """Create REST API with 3 endpoints."""
        
        # Main API Gateway
        self.api = apigateway.RestApi(
            self, "TrendScribeAPI",
            rest_api_name="TrendScribe API",
            description="API for TrendScribe - AI Video Script Generator",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["Content-Type", "Authorization"]
            )
        )
        
        # POST /content/process
        content_resource = self.api.root.add_resource("content")
        process_resource = content_resource.add_resource("process")
        process_integration = apigateway.LambdaIntegration(self.content_processor_lambda)
        process_resource.add_method("POST", process_integration)
        
        # POST /trends/analyze
        trends_resource = self.api.root.add_resource("trends")
        analyze_resource = trends_resource.add_resource("analyze")
        analyze_integration = apigateway.LambdaIntegration(self.trend_analyzer_lambda)
        analyze_resource.add_method("POST", analyze_integration)
        
        # POST /scripts/generate
        scripts_resource = self.api.root.add_resource("scripts")
        generate_resource = scripts_resource.add_resource("generate")
        generate_integration = apigateway.LambdaIntegration(self.script_generator_lambda)
        generate_resource.add_method("POST", generate_integration)

    # ========================================================================
    # COGNITO USER POOL
    # ========================================================================

    def _create_cognito_pool(self):
        """Create Cognito User Pool for authentication."""
        
        self.user_pool = cognito.UserPool(
            self, "TrendScribeUserPool",
            user_pool_name="trendscribe-users",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(
                username=True,
                email=True
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=12,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False
            )
        )
        
        # App client for frontend
        self.user_pool_client = self.user_pool.add_client(
            "TrendScribeAppClient",
            auth_flows=cognito.AuthFlow(
                user_password=True,
                admin_user_password=True,
                allow_refresh_token_based_auth=True
            ),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    implicit_code_grant=True
                ),
                scopes=[cognito.OAuthScope.OPENID, cognito.OAuthScope.PROFILE, cognito.OAuthScope.EMAIL]
            )
        )

    # ========================================================================
    # CLOUDWATCH LOG GROUPS
    # ========================================================================

    def _create_cloudwatch_logs(self):
        """Create CloudWatch log groups for Lambda functions."""
        
        logs.LogGroup(
            self, "ContentProcessorLogs",
            log_group_name=f"/aws/lambda/content-processor-{self.env_name}",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        logs.LogGroup(
            self, "TrendAnalyzerLogs",
            log_group_name=f"/aws/lambda/trend-analyzer-{self.env_name}",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        logs.LogGroup(
            self, "ScriptGeneratorLogs",
            log_group_name=f"/aws/lambda/script-generator-{self.env_name}",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY
        )

    # ========================================================================
    # STACK OUTPUTS
    # ========================================================================

    def _output_resource_info(self):
        """Output stack resource information."""
        
        core.CfnOutput(
            self, "ApiEndpoint",
            value=self.api.url,
            description="API Gateway Endpoint"
        )
        
        core.CfnOutput(
            self, "UserPoolId",
            value=self.user_pool.user_pool_id,
            description="Cognito User Pool ID"
        )
        
        core.CfnOutput(
            self, "S3BucketName",
            value=self.s3_bucket.bucket_name,
            description="S3 Bucket for Content and Scripts"
        )


# ============================================================================
# APP ENTRY POINT
# ============================================================================

def create_trendscribe_app():
    """Create and return the CDK App with TrendScribe stack."""
    
    app = core.App()
    
    env_name = os.getenv('ENVIRONMENT', 'dev')
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    TrendScribeStack(
        app, "TrendScribeStack",
        env=core.Environment(region=region),
        description="TrendScribe - AI Video Script Generator"
    )
    
    return app


if __name__ == "__main__":
    """
    CDK Stack Deployments:
    - Install CDK: pip install aws-cdk-lib
    - Configure AWS credentials: aws configure
    - Deploy: cdk deploy
    - Destroy: cdk destroy
    """
    
    print("\nTrendScribe CDK Stack")
    print("="*60)
    print("\nUsage:")
    print("  cdk synth     - Generate CloudFormation template")
    print("  cdk deploy    - Deploy to AWS")
    print("  cdk destroy   - Remove all resources")
    print("\nEnvironment Variables:")
    print("  AWS_REGION    - AWS region (default: us-east-1)")
    print("  ENVIRONMENT   - Environment name (default: dev)")
    print("="*60 + "\n")
    
    app = create_trendscribe_app()
    app.synth()
