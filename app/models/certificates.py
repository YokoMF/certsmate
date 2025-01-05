from app import db


class Certificate(db.Base):
    __tablename__ = "certificates"

    # 主键，UUID 类型
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    # 证书名称
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # 域名
    domain: Mapped[str] = mapped_column(String(255), nullable=False)

    # 云服务商
    cloud_provider: Mapped[str] = mapped_column(String(50), nullable=False)

    # 到期日期
    expiration_date: Mapped[datetime] = mapped_column(Date, nullable=False)

    # 证书文件路径
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)

    # 状态（如有效、过期）
    status: Mapped[str] = mapped_column(String(50), default="valid")

    # 创建时间
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # 更新时间
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # 关系：与日志表一对多
    logs: Mapped[list["OperationLog"]] = relationship(
        back_populates="certificate", cascade="all, delete-orphan"
    )